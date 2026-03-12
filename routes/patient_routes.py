from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from models.patient_model import Patient
from models.appointment_model import Appointment
from models.medical_record_model import MedicalRecord
from models.doctor_model import Doctor
import logging

patient_bp = Blueprint('patient', __name__)
logger = logging.getLogger(__name__)

@patient_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    try:
        if request.method == 'GET':
            # If user opens signup again, start a fresh registration session.
            session.pop('patient_id', None)
            session.pop('patient_name', None)

        if request.method == 'POST':
            data = request.form
            email = Patient.normalize_email(data.get('email'))
            
            # Check if patient already exists
            existing_patient = Patient.find_by_email(email)
            if existing_patient:
                flash('Email already registered. Please login or use a different email.', 'warning')
                return redirect(url_for('patient.register'))
            
            patient = Patient(
                name=data['name'],
                age=int(data['age']),
                gender=data['gender'],
                contact_number=data['contact_number'],
                email=email,
                password=data['password']
            )
            patient.save()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('patient.login'))
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        flash(f'Registration error: {str(e)}', 'error')
        return redirect(url_for('patient.register'))
    return render_template('register.html', error=error)

@patient_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    email_value = ''
    try:
        if request.method == 'POST':
            email = Patient.normalize_email(request.form.get('email', ''))
            password = request.form.get('password', '')
            email_value = email
            
            if not email or not password:
                error = 'Please provide both email and password.'
            else:
                patient = Patient.find_by_email(email)
                if patient and Patient.verify_password(patient['password'], password):
                    session['patient_id'] = str(patient['_id'])
                    session['patient_name'] = patient['name']
                    flash('Login successful!', 'success')
                    return redirect(url_for('patient.dashboard'))
                else:
                    error = 'Invalid email or password. Please try again.'
    except Exception as e:
        error = f'Login error: {str(e)}'
        logger.error(f"Login error: {str(e)}")
    
    return render_template('login.html', error=error, email_value=email_value)

@patient_bp.route('/dashboard')
def dashboard():
    if 'patient_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('patient.login'))

    try:
        patient_id = session['patient_id']
        appointments = Appointment.find_by_patient(patient_id)
        records = MedicalRecord.find_by_patient(patient_id)
        return render_template('patient_dashboard.html', appointments=appointments, records=records)
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        flash('Error loading dashboard. Please try again.', 'error')
        return redirect(url_for('patient.login'))


@patient_bp.route('/appointments')
def booked_appointments():
    if 'patient_id' not in session:
        flash('Please login first.', 'warning')
        return redirect(url_for('patient.login'))

    try:
        patient_id = session['patient_id']
        appointments = Appointment.find_by_patient(patient_id)
        booked = [a for a in appointments if str(a.get('status', '')).strip().lower() == 'booked']

        detailed_appointments = []
        for appointment in booked:
            item = dict(appointment)
            doctor = Doctor.find_by_id(item.get('doctor_id'))
            item['doctor_name'] = doctor.get('name') if doctor else 'Unknown Doctor'
            item['doctor_specialization'] = doctor.get('specialization') if doctor else 'N/A'
            detailed_appointments.append(item)

        return render_template('patient_booked_appointments.html', appointments=detailed_appointments)
    except Exception as e:
        logger.error(f"Booked appointments error: {str(e)}")
        flash('Error loading booked appointments. Please try again.', 'error')
        return redirect(url_for('patient.dashboard'))

@patient_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))