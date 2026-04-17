@echo off
REM CloseZap AI - Windows Startup Script

echo ================================================
echo CloseZap AI - Starting Development Server
echo ================================================

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Change to script directory
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Create .env if not exists
if not exist ".env" (
    if exist ".env.example" (
        echo Creating .env from .env.example...
        copy .env.example .env
        echo Please edit .env with your credentials!
    )
)

REM Run server
echo.
echo ================================================
echo Server starting at http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ================================================
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause