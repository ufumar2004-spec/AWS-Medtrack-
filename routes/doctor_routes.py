from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from models.doctor_model import Doctor
from models.appointment_model import Appointment
from models.medical_record_model import MedicalRecord
from models.patient_model import Patient
from database.mongodb import mongo

doctor_bp = Blueprint('doctor', __name__)


def _seed_default_doctors_if_empty():
    default_doctors = [
        {
            'name': 'Dr. John Smith',
            'specialization': 'Cardiologist',
            'experience': 10,
            'availability': 'Mon-Fri 9AM-5PM',
            'email': 'john.smith@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. Sarah Johnson',
            'specialization': 'Dermatologist',
            'experience': 8,
            'availability': 'Tue-Sat 10AM-6PM',
            'email': 'sarah.johnson@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. Michael Brown',
            'specialization': 'Orthopedic Surgeon',
            'experience': 12,
            'availability': 'Mon-Thu 8AM-4PM',
            'email': 'michael.brown@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. Emily Davis',
            'specialization': 'Pediatrician',
            'experience': 9,
            'availability': 'Mon-Fri 11AM-7PM',
            'email': 'emily.davis@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. William Garcia',
            'specialization': 'Neurologist',
            'experience': 14,
            'availability': 'Mon-Wed 9AM-3PM',
            'email': 'william.garcia@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. Olivia Martinez',
            'specialization': 'Gynecologist',
            'experience': 11,
            'availability': 'Tue-Fri 8AM-2PM',
            'email': 'olivia.martinez@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. James Wilson',
            'specialization': 'ENT Specialist',
            'experience': 7,
            'availability': 'Mon-Sat 1PM-8PM',
            'email': 'james.wilson@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. Ava Anderson',
            'specialization': 'Psychiatrist',
            'experience': 13,
            'availability': 'Wed-Sun 10AM-6PM',
            'email': 'ava.anderson@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. Benjamin Thomas',
            'specialization': 'Oncologist',
            'experience': 15,
            'availability': 'Mon-Fri 7AM-1PM',
            'email': 'benjamin.thomas@medtrack.com',
            'password': 'password123'
        },
        {
            'name': 'Dr. Sophia Taylor',
            'specialization': 'General Physician',
            'experience': 6,
            'availability': 'Daily 9AM-5PM',
            'email': 'sophia.taylor@medtrack.com',
            'password': 'password123'
        }
    ]

    inserted_count = 0
    for doc in default_doctors:
        exists = mongo.db.doctors.find_one({'email': doc['email']})
        if not exists:
            Doctor(**doc).save()
            inserted_count += 1

    return inserted_count

@doctor_bp.route('/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        data = request.form
        doctor = Doctor(
            name=data['name'],
            specialization=data['specialization'],
            experience=int(data['experience']),
            availability=data['availability'],
            email=data['email'],
            password=data['password']
        )
        doctor.save()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_doctor.html')

@doctor_bp.route('/list')
def list_doctors():
    inserted_count = _seed_default_doctors_if_empty()
    doctors = Doctor.find_all()
    if inserted_count:
        flash(f'{inserted_count} doctor records were added to complete the directory.', 'info')
    return render_template('doctor_list.html', doctors=doctors)


@doctor_bp.route('/contact/<doctor_id>', methods=['GET', 'POST'])
def contact_doctor(doctor_id):
    doctor = Doctor.find_by_id(doctor_id)
    if not doctor:
        flash('Doctor not found.', 'error')
        return redirect(url_for('doctor.list_doctors'))

    if request.method == 'POST':
        sender_name = request.form.get('name', '').strip()
        sender_email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not sender_name or not sender_email or not message:
            flash('Please fill out all contact fields.', 'warning')
            return render_template('contact_doctor.html', doctor=doctor)

        # In this local flow, we confirm request submission via UI feedback.
        flash(f"Your message has been sent to {doctor['name']}.", 'success')
        return redirect(url_for('doctor.contact_doctor', doctor_id=doctor_id))

    return render_template('contact_doctor.html', doctor=doctor)

@doctor_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        doctor = Doctor.find_by_email(email)
        if doctor and Doctor.verify_password(doctor['password'], password):
            session['doctor_id'] = str(doctor['_id'])
            return redirect(url_for('doctor.dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('doctor.login'))
    
    return render_template('doctor_login.html')

@doctor_bp.route('/logout')
def logout():
    session.pop('doctor_id', None)
    return redirect(url_for('doctor.login'))

@doctor_bp.route('/dashboard')
def dashboard():
    if 'doctor_id' not in session:
        return redirect(url_for('doctor.login'))
    
    doctor_id = session['doctor_id']
    doctor = Doctor.find_by_id(doctor_id)
    if not doctor:
        session.pop('doctor_id', None)
        return redirect(url_for('doctor.login'))
    
    appointments = Appointment.find_by_doctor(doctor_id)
    total_appointments = len(appointments)
    upcoming_appointments = [appt for appt in appointments if appt['status'] == 'Booked']
    
    return render_template('doctor_dashboard.html', 
                         doctor=doctor, 
                         total_appointments=total_appointments, 
                         upcoming_appointments=upcoming_appointments)

@doctor_bp.route('/appointments')
def view_appointments():
    if 'doctor_id' not in session:
        return redirect(url_for('doctor.login'))
    
    doctor_id = session['doctor_id']
    appointments = Appointment.find_by_doctor(doctor_id)
    
    # Get patient details for each appointment
    appointments_with_patients = []
    for appt in appointments:
        patient = Patient.find_by_id(appt['patient_id'])
        if patient:
            appt_with_patient = dict(appt)
            appt_with_patient['patient_name'] = patient['name']
            appt_with_patient['patient_age'] = patient['age']
            appt_with_patient['patient_contact'] = patient['contact_number']
            appointments_with_patients.append(appt_with_patient)
    
    return render_template('doctor_appointments.html', appointments=appointments_with_patients)

@doctor_bp.route('/patient/<patient_id>')
def view_patient_details(patient_id):
    if 'doctor_id' not in session:
        return redirect(url_for('doctor.login'))
    
    patient = Patient.find_by_id(patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('doctor.appointments'))
    
    medical_records = MedicalRecord.find_by_patient(patient_id)
    
    return render_template('patient_details.html', patient=patient, medical_records=medical_records)

@doctor_bp.route('/add_record/<patient_id>', methods=['GET', 'POST'])
def add_record(patient_id):
    if 'doctor_id' not in session:
        return redirect(url_for('doctor.login'))
    
    doctor_id = session['doctor_id']
    
    if request.method == 'POST':
        diagnosis = request.form['diagnosis']
        prescription = request.form['prescription']
        notes = request.form['notes']
        
        record = MedicalRecord(
            patient_id=patient_id,
            doctor_id=doctor_id,
            diagnosis=diagnosis,
            prescription=prescription,
            notes=notes
        )
        record.save()
        
        # Update appointment status to completed if exists
        appointment = mongo.db.appointments.find_one({'patient_id': patient_id, 'doctor_id': doctor_id, 'status': 'Booked'})
        if appointment:
            Appointment.update_status(str(appointment['_id']), 'Completed')
        
        flash('Medical record added successfully', 'success')
        return redirect(url_for('doctor.view_patient_details', patient_id=patient_id))
    
    patient = Patient.find_by_id(patient_id)
    return render_template('add_record.html', patient=patient)