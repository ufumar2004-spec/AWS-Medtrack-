from app import mongo
from models.doctor_model import Doctor

# Sample doctors
doctors = [
    {
        'name': 'Dr. John Smith', 
        'specialization': 'Cardiology', 
        'experience': 10, 
        'availability': 'Mon-Fri 9AM-5PM',
        'email': 'john.smith@medtrack.com',
        'password': 'password123'
    },
    {
        'name': 'Dr. Sarah Johnson', 
        'specialization': 'Dermatology', 
        'experience': 8, 
        'availability': 'Tue-Sat 10AM-6PM',
        'email': 'sarah.johnson@medtrack.com',
        'password': 'password123'
    },
    {
        'name': 'Dr. Michael Brown', 
        'specialization': 'Orthopedics', 
        'experience': 12, 
        'availability': 'Mon-Thu 8AM-4PM',
        'email': 'michael.brown@medtrack.com',
        'password': 'password123'
    }
]

for doc in doctors:
    doctor = Doctor(**doc)
    doctor.save()

print("Sample doctors added successfully!")