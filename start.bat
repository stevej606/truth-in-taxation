@echo off
echo ==========================================
echo Truth-in-Taxation Forms Portal
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python version:
python --version

REM Check if virtual environment exists
if not exist "venv\" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade requirements
echo.
echo Installing dependencies...
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
echo Dependencies installed

REM Start the server
echo.
echo ==========================================
echo Starting Flask server...
echo ==========================================
echo.
echo Server will be available at:
echo   - http://localhost:5000
echo.
echo Open truth-in-taxation-complete.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

python server.py
