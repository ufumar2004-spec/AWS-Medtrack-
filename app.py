from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from database.mongodb import mongo
from routes.patient_routes import patient_bp
from routes.doctor_routes import doctor_bp
from routes.appointment_routes import appointment_bp
from models.appointment_model import Appointment
from models.patient_model import Patient
from models.doctor_model import Doctor
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DynamoDB
try:
    mongo.init_app(app)
    # Test configured database backend
    mongo.db.command('ping')
    if getattr(mongo, 'backend', 'dynamodb') == 'memory':
        print("[WARN] DynamoDB unavailable. Running with in-memory fallback backend.")
    else:
        print("[OK] DynamoDB connection successful")
except Exception as e:
    print(f"[ERROR] DynamoDB connection failed: {str(e)}")
    print("Please ensure AWS credentials and DynamoDB access are configured.")
    exit(1)

app.register_blueprint(patient_bp, url_prefix='/patient')
app.register_blueprint(doctor_bp, url_prefix='/doctor')
app.register_blueprint(appointment_bp, url_prefix='/appointment')

@app.route('/')
def index():
    try:
        total_patients = len(Patient.find_all())
        total_doctors = mongo.db.doctors.count_documents({})
        upcoming_appointments = len(Appointment.find_upcoming())
        return render_template('index.html', total_patients=total_patients, total_doctors=total_doctors, upcoming_appointments=upcoming_appointments)
    except Exception as e:
        app.logger.error(f"Database error: {str(e)}")
        flash('Database connection error. Please try again later.', 'error')
        return render_template('index.html', total_patients=0, total_doctors=0, upcoming_appointments=0)


@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Disable the reloader to avoid multi-process behavior with in-memory fallback data.
    app.run(debug=Config.DEBUG, host='0.0.0.0', use_reloader=False)