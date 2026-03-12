# MedTrack Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MedTrack Healthcare Management System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Check MongoDB
Write-Host "Checking MongoDB connection..." -NoNewline
try {
    $mongoCheck = netstat -ano | findstr :27017
    if ($mongoCheck) {
        Write-Host " ✅ MongoDB is running" -ForegroundColor Green
    } else {
        Write-Host " ❌ MongoDB not found" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please start MongoDB:" -ForegroundColor Yellow
        Write-Host "1. Open PowerShell as Administrator"
        Write-Host "2. Run: Start-Service MongoDB"
        Write-Host "3. Or start mongod.exe manually"
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host " ❌ Error checking MongoDB" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Green
Write-Host "Access at: http://127.0.0.1:5000/" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start Flask app
python app.py

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"