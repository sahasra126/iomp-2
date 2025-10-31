# PCOS Predictor - Quick Setup Script (Windows)
# Run this script to set up the project automatically

Write-Host "🌸 PCOS Predictor - Quick Setup Script" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion found" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js $nodeVersion found" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "Checking PostgreSQL installation..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "✅ $pgVersion found" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PostgreSQL command line tools not found" -ForegroundColor Yellow
    Write-Host "   Please ensure PostgreSQL is installed and running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Step 1: Setting up Backend" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Backend setup
Set-Location backend

Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "✅ Backend dependencies installed!" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  IMPORTANT: Configure your database" -ForegroundColor Yellow
Write-Host "   1. Copy .env.example to .env" -ForegroundColor White
Write-Host "   2. Update database credentials in .env" -ForegroundColor White
Write-Host "   3. Create database: CREATE DATABASE pcos_db;" -ForegroundColor White
Write-Host ""

# Return to root
Set-Location ..

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host "Step 2: Setting up Frontend" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

Set-Location frontend

Write-Host "Installing Node.js dependencies (this may take a few minutes)..." -ForegroundColor Yellow
npm install

Write-Host ""
Write-Host "✅ Frontend dependencies installed!" -ForegroundColor Green

# Return to root
Set-Location ..

Write-Host ""
Write-Host "=======================================" -ForegroundColor Green
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Create PostgreSQL database:" -ForegroundColor White
Write-Host "   psql -U postgres -c 'CREATE DATABASE pcos_db;'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Configure backend/.env with your database credentials" -ForegroundColor White
Write-Host ""
Write-Host "3. Start the backend server:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. In a new terminal, start the frontend:" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm start" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Open your browser to http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see README.md" -ForegroundColor Yellow
Write-Host ""
