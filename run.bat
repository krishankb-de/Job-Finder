@echo off
REM Job Finder Quick Start Script for Windows

echo.
echo ====================================================================
echo                    JOB FINDER FOR GERMAN COMPANIES
echo ====================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo Step 1: Checking Python installation...
python --version
echo OK
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Step 2: Creating virtual environment...
    python -m venv venv
    echo OK
    echo.
    
    echo Step 3: Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo OK
    echo.
) else (
    echo Step 2: Activating existing virtual environment...
    call venv\Scripts\activate.bat
    echo OK
    echo.
)

echo Step 3: Starting Job Finder...
echo.
echo ====================================================================
echo                        SEARCH IN PROGRESS
echo ====================================================================
echo.

python main.py

echo.
echo ====================================================================
echo                         SEARCH COMPLETED
echo ====================================================================
echo.
echo Results have been saved to the 'output' folder
echo Check job_finder.log for detailed information
echo.

pause
