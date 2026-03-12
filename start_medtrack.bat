@echo off
echo Starting MedTrack Healthcare Management System...
echo.

REM Check if MongoDB is running
netstat -ano | findstr :27017 >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: MongoDB is not running!
    echo Please start MongoDB first:
    echo 1. Open a new terminal as Administrator
    echo 2. Run: net start MongoDB
    echo Or start mongod.exe manually
    pause
    exit /b 1
)

echo MongoDB is running ✓
echo.

REM Change to the correct directory
cd /d d:\AWS\medtrack

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    pause
    exit /b 1
)

echo Starting Flask application...
echo Access the application at: http://127.0.0.1:5000/
echo Press Ctrl+C to stop the server
echo.

python app.py

echo.
echo Flask application stopped.
pause