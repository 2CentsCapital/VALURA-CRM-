@echo off
REM Valura CRM Dashboard - Run Server Script

echo ============================================
echo Starting Valura CRM Dashboard Server...
echo ============================================
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Using Excel files for data (hardcoded mode)
echo Excel files: Freshsales Contacts.xlsx, Investment Opportunities.xlsx
echo.

echo Starting FastAPI server...
echo.
echo Dashboard will be available at: http://127.0.0.1:8000
echo API Documentation at: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
