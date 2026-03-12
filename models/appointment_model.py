from database.mongodb import mongo

class Appointment:
    def __init__(self, patient_id, doctor_id, date, time, status='Booked'):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.status = status

    def save(self):
        appointment_data = {
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
            'time': self.time,
            'status': self.status
        }
        return mongo.db.appointments.insert_one(appointment_data)

    @staticmethod
    def find_by_patient(patient_id):
        return list(mongo.db.appointments.find({'patient_id': patient_id}))

    @staticmethod
    def find_by_doctor(doctor_id):
        return list(mongo.db.appointments.find({'doctor_id': doctor_id}))

    @staticmethod
    def find_upcoming():
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        return list(mongo.db.appointments.find({'date': {'$gte': today}, 'status': 'Booked'}))

    @staticmethod
    def update_status(appointment_id, status):
        return mongo.db.appointments.update_one({'_id': str(appointment_id)}, {'$set': {'status': status}})