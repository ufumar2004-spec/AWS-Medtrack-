# MedTrack - Healthcare Management System

A comprehensive web-based healthcare management system built with Flask and DynamoDB.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- AWS credentials with DynamoDB access (or DynamoDB Local)
- Windows OS

### 1. Configure DynamoDB
Set environment variables before running:

```bash
set AWS_REGION=us-east-1
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set DYNAMODB_TABLE_PREFIX=medtrack_

# Optional (for DynamoDB Local)
set DYNAMODB_ENDPOINT_URL=http://localhost:8000
```

### 2. Run the Application
```bash
# Double-click the batch file
start_medtrack.bat

# Or run manually:
cd d:\AWS\medtrack
python app.py
```

### 3. Access the Application
- Open browser: `http://127.0.0.1:5000/`
- Register a new patient account
- Login and start using the system

## 📋 Features

- ✅ Patient Registration & Login
- ✅ Doctor Management
- ✅ Appointment Booking
- ✅ Medical Records Management
- ✅ Professional Healthcare UI
- ✅ Responsive Design
- ✅ Error Handling

## 🛠 Troubleshooting

### "Application won't start"
1. Ensure AWS credentials are set: `echo %AWS_ACCESS_KEY_ID%`
2. If using DynamoDB Local, verify it is running: `netstat -ano | findstr :8000`
2. Check Python installation: `python --version`
3. Run the batch file: `start_medtrack.bat`

### "500 Internal Server Error"
- Check browser console for details
- Ensure all dependencies are installed
- Verify MongoDB connection

### "Port already in use"
- Kill existing process: `taskkill /PID <PID> /F`
- Or change port in app.py

## 📁 Project Structure

```
medtrack/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── start_medtrack.bat    # Startup script
├── models/               # Database models
├── routes/               # Flask routes
├── templates/            # HTML templates
├── static/               # CSS, JS files
└── database/             # Database connection
```

## 🔧 Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run in Debug Mode
```bash
set FLASK_ENV=development
python app.py
```

### Database
- Collections: patients, doctors, appointments, medical_records
- Database: AWS DynamoDB
- Table naming: `<DYNAMODB_TABLE_PREFIX>{patients|doctors|appointments|medical_records}`

## 🚀 Deployment

Ready for AWS deployment.

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Ensure all prerequisites are met
3. Run the startup batch file for automated checks