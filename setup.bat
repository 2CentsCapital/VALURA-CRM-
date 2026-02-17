@echo off
REM Valura CRM Dashboard - Setup Script

echo ============================================
echo Valura CRM Dashboard Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo.
    echo [2/4] Creating virtual environment...
    python -m venv venv
) else (
    echo.
    echo [2/4] Virtual environment already exists
)

REM Activate virtual environment
echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo [4/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Currently using hardcoded data from Excel files:
echo - Freshsales Contacts.xlsx
echo - Investment Opportunities.xlsx
echo.
echo To start the server:
echo   1. Run: run.bat
echo   2. Open browser: http://127.0.0.1:8000
echo.
echo Note: .env file is optional (will be needed for API integration later)
echo.
pause
