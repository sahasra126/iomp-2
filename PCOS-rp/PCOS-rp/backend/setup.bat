@echo off
echo ================================
echo PCOS Predictor - Backend Setup
echo ================================
echo.

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Checking for .env file...
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit .env file and set your PostgreSQL password!
    echo.
) else (
    echo .env file already exists
)

echo [5/5] Training model if needed...
if not exist pcos_model.pkl (
    echo Training model...
    python train_model.py
) else (
    echo Model already exists
)

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Create PostgreSQL database: CREATE DATABASE pcos_db;
echo 2. Edit .env file with your database credentials
echo 3. Run: python app_with_auth.py
echo.
pause
