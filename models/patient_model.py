from database.mongodb import mongo
import bcrypt

class Patient:
    def __init__(self, name, age, gender, contact_number, email, password):
        self.name = name
        self.age = age
        self.gender = gender
        self.contact_number = contact_number
        self.email = self.normalize_email(email)
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def normalize_email(email):
        if email is None:
            return ''
        return str(email).strip().lower()

    def save(self):
        patient_data = {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'contact_number': self.contact_number,
            'email': self.email,
            'password': self.password
        }
        return mongo.db.patients.insert_one(patient_data)

    @staticmethod
    def find_by_email(email):
        normalized_email = Patient.normalize_email(email)
        patient = mongo.db.patients.find_one({'email': normalized_email})
        if patient:
            return patient

        # Backward compatibility for records saved before normalization.
        for item in mongo.db.patients.find():
            if Patient.normalize_email(item.get('email')) == normalized_email:
                return item
        return None

    @staticmethod
    def find_all():
        return list(mongo.db.patients.find())

    @staticmethod
    def find_by_id(patient_id):
        return mongo.db.patients.find_one({'_id': str(patient_id)})

    @staticmethod
    def verify_password(stored_password, provided_password):
        if not stored_password or provided_password is None:
            return False

        try:
            # Preferred path: bcrypt hashed password
            return bcrypt.checkpw(
                provided_password.encode('utf-8'),
                stored_password.encode('utf-8')
            )
        except Exception:
            # Backward compatibility for any legacy plain-text records
            return stored_password == provided_password