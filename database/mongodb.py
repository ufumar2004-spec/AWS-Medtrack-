import uuid
from datetime import datetime
from decimal import Decimal

import boto3


def _normalize_scalar(value):
	if isinstance(value, Decimal):
		if value % 1 == 0:
			return int(value)
		return float(value)
	return value


def _serialize_value(value):
	if isinstance(value, datetime):
		return value.isoformat()
	if isinstance(value, dict):
		return {k: _serialize_value(v) for k, v in value.items()}
	if isinstance(value, list):
		return [_serialize_value(v) for v in value]
	return value


def _deserialize_value(value):
	if isinstance(value, dict):
		return {k: _deserialize_value(v) for k, v in value.items()}
	if isinstance(value, list):
		return [_deserialize_value(v) for v in value]
	return _normalize_scalar(value)


def _match_filter(item, filters):
	if not filters:
		return True

	for key, expected in filters.items():
		actual = item.get(key)
		if isinstance(expected, dict):
			if '$gte' in expected:
				target = expected['$gte']
				if actual is None or actual < target:
					return False
			else:
				return False
		else:
			if str(actual) != str(expected):
				return False
	return True


class InsertResult:
	def __init__(self, inserted_id):
		self.inserted_id = inserted_id


class UpdateResult:
	def __init__(self, modified_count):
		self.modified_count = modified_count


class DynamoCollection:
	def __init__(self, db, collection_name):
		self._db = db
		self._collection_name = collection_name

	@property
	def _table_name(self):
		return f"{self._db.table_prefix}{self._collection_name}"

	@property
	def _table(self):
		return self._db.resource.Table(self._table_name)

	def insert_one(self, data):
		item = dict(data)
		item['_id'] = item.get('_id') or str(uuid.uuid4())
		self._table.put_item(Item=_serialize_value(item))
		return InsertResult(item['_id'])

	def find(self, filters=None):
		response = self._table.scan()
		items = response.get('Items', [])
		while 'LastEvaluatedKey' in response:
			response = self._table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
			items.extend(response.get('Items', []))

		normalized = [_deserialize_value(item) for item in items]
		return [item for item in normalized if _match_filter(item, filters or {})]

	def find_one(self, filters=None):
		matches = self.find(filters or {})
		return matches[0] if matches else None

	def count_documents(self, filters=None):
		return len(self.find(filters or {}))

	def update_one(self, filters, update):
		item = self.find_one(filters)
		if not item:
			return UpdateResult(0)

		set_values = update.get('$set', {}) if isinstance(update, dict) else {}
		item.update(set_values)
		self._table.put_item(Item=_serialize_value(item))
		return UpdateResult(1)


class DynamoDatabaseProxy:
	def __init__(self, db):
		self._db = db

	def __getattr__(self, collection_name):
		return DynamoCollection(self._db, collection_name)

	def command(self, command_name):
		if command_name == 'ping':
			self._db.resource.meta.client.list_tables(Limit=1)
			return {'ok': 1}
		raise ValueError(f'Unsupported command: {command_name}')


class MemoryCollection:
	def __init__(self, db, collection_name):
		self._db = db
		self._collection_name = collection_name

	@property
	def _bucket(self):
		if self._collection_name not in self._db._memory_store:
			self._db._memory_store[self._collection_name] = {}
		return self._db._memory_store[self._collection_name]

	def insert_one(self, data):
		item = dict(data)
		item['_id'] = item.get('_id') or str(uuid.uuid4())
		self._bucket[item['_id']] = _deserialize_value(_serialize_value(item))
		return InsertResult(item['_id'])

	def find(self, filters=None):
		items = list(self._bucket.values())
		return [item for item in items if _match_filter(item, filters or {})]

	def find_one(self, filters=None):
		matches = self.find(filters or {})
		return matches[0] if matches else None

	def count_documents(self, filters=None):
		return len(self.find(filters or {}))

	def update_one(self, filters, update):
		item = self.find_one(filters)
		if not item:
			return UpdateResult(0)

		set_values = update.get('$set', {}) if isinstance(update, dict) else {}
		item.update(set_values)
		self._bucket[item['_id']] = item
		return UpdateResult(1)


class MemoryDatabaseProxy:
	def __init__(self, db):
		self._db = db

	def __getattr__(self, collection_name):
		return MemoryCollection(self._db, collection_name)

	def command(self, command_name):
		if command_name == 'ping':
			return {'ok': 1, 'backend': 'memory'}
		raise ValueError(f'Unsupported command: {command_name}')


class DynamoDB:
	def __init__(self):
		self.resource = None
		self.db = None
		self.table_prefix = ''
		self.backend = 'dynamodb'
		self._memory_store = {}

	def init_app(self, app):
		region = app.config.get('AWS_REGION', 'us-east-1')
		endpoint_url = app.config.get('DYNAMODB_ENDPOINT_URL')
		table_prefix = app.config.get('DYNAMODB_TABLE_PREFIX', '')
		self.table_prefix = table_prefix

		try:
			self.resource = boto3.resource(
				'dynamodb',
				region_name=region,
				endpoint_url=endpoint_url,
				aws_access_key_id=app.config.get('AWS_ACCESS_KEY_ID'),
				aws_secret_access_key=app.config.get('AWS_SECRET_ACCESS_KEY')
			)
			self.db = DynamoDatabaseProxy(self)
			self._ensure_tables()
			self.backend = 'dynamodb'
		except Exception:
			# Fallback mode keeps the app runnable for local UI development.
			self.resource = None
			self.db = MemoryDatabaseProxy(self)
			self.backend = 'memory'

	def _ensure_tables(self):
		required_tables = ['patients', 'doctors', 'appointments', 'medical_records']
		client = self.resource.meta.client
		existing = set(client.list_tables().get('TableNames', []))

		for collection_name in required_tables:
			table_name = f"{self.table_prefix}{collection_name}"
			if table_name in existing:
				continue

			self.resource.create_table(
				TableName=table_name,
				KeySchema=[{'AttributeName': '_id', 'KeyType': 'HASH'}],
				AttributeDefinitions=[{'AttributeName': '_id', 'AttributeType': 'S'}],
				BillingMode='PAY_PER_REQUEST'
			)

		for collection_name in required_tables:
			table_name = f"{self.table_prefix}{collection_name}"
			self.resource.Table(table_name).wait_until_exists()


mongo = DynamoDB()