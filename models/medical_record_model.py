from database.mongodb import mongo
from datetime import datetime

class MedicalRecord:
    def __init__(self, patient_id, doctor_id, diagnosis, prescription, notes):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.notes = notes
        self.date = datetime.now()

    def save(self):
        record_data = {
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'notes': self.notes,
            'date': self.date
        }
        return mongo.db.medical_records.insert_one(record_data)

    @staticmethod
    def find_by_patient(patient_id):
        return list(mongo.db.medical_records.find({'patient_id': patient_id}))