import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    AWS_REGION = os.environ.get('AWS_REGION') or 'us-east-1'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    DYNAMODB_ENDPOINT_URL = os.environ.get('DYNAMODB_ENDPOINT_URL')
    DYNAMODB_TABLE_PREFIX = os.environ.get('DYNAMODB_TABLE_PREFIX') or 'medtrack_'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'