@echo off
echo AI-Powered Lost & Found System - Windows Setup
echo ==============================================

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo.
    echo Please install Python first:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download and install Python 3.11 or 3.12
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Run this script again after installation
    echo.
    pause
    exit /b 1
)

echo Python found!
python --version

echo.
echo Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Package installation failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Running system tests...
python test_system.py

if %errorlevel% neq 0 (
    echo.
    echo Some tests failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo To start the server, run:
echo   python start_server.py
echo.
echo Or test the system with:
echo   python example_usage.py
echo.
pause


