@echo off
echo ========================================
echo   MedTrack Healthcare Management System
echo ========================================
echo.
echo Starting application...
echo.

REM Change to the project directory
cd /d "%~dp0"

REM Check if MongoDB is running
echo Checking MongoDB connection...
netstat -ano | findstr :27017 >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: MongoDB is not running!
    echo.
    echo Please start MongoDB first:
    echo 1. Open Command Prompt as Administrator
    echo 2. Run: net start MongoDB
    echo 3. Or start mongod.exe manually
    echo.
    pause
    exit /b 1
)

echo ✅ MongoDB is running
echo.

REM Start the Flask application
echo Starting Flask server...
echo Access at: http://127.0.0.1:5000/
echo Press Ctrl+C to stop
echo.
python app.py

echo.
echo Server stopped.
pause