from database.mongodb import mongo
import bcrypt

class Doctor:
    def __init__(self, name, specialization, experience, availability, email, password):
        self.name = name
        self.specialization = specialization
        self.experience = experience
        self.availability = availability
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def save(self):
        doctor_data = {
            'name': self.name,
            'specialization': self.specialization,
            'experience': self.experience,
            'availability': self.availability,
            'email': self.email,
            'password': self.password
        }
        return mongo.db.doctors.insert_one(doctor_data)

    @staticmethod
    def find_all():
        return list(mongo.db.doctors.find())

    @staticmethod
    def find_by_id(doctor_id):
        return mongo.db.doctors.find_one({'_id': str(doctor_id)})

    @staticmethod
    def find_by_email(email):
        return mongo.db.doctors.find_one({'email': email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))