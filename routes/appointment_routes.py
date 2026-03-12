from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models.appointment_model import Appointment
from models.doctor_model import Doctor

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/book', methods=['GET', 'POST'])
def book():
    if 'patient_id' not in session:
        return redirect(url_for('patient.login'))
    if request.method == 'POST':
        data = request.form
        appointment = Appointment(
            patient_id=session['patient_id'],
            doctor_id=data['doctor_id'],
            appointment_date=data['date'],
            appointment_time=data['time']
        )
        appointment.save()
        return redirect(url_for('patient.dashboard'))
    doctors = Doctor.find_all()
    return render_template('book_appointment.html', doctors=doctors)