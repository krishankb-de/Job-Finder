#!/bin/bash
# Job Finder Quick Start Script for macOS/Linux

echo ""
echo "===================================================================="
echo "                    JOB FINDER FOR GERMAN COMPANIES"
echo "===================================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org"
    exit 1
fi

echo "Step 1: Checking Python installation..."
python3 --version
echo "OK"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Step 2: Creating virtual environment..."
    python3 -m venv venv
    echo "OK"
    echo ""
    
    echo "Step 3: Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    echo "OK"
    echo ""
else
    echo "Step 2: Activating existing virtual environment..."
    source venv/bin/activate
    echo "OK"
    echo ""
fi

echo "Step 3: Starting Job Finder..."
echo ""
echo "===================================================================="
echo "                        SEARCH IN PROGRESS"
echo "===================================================================="
echo ""

python3 main.py

echo ""
echo "===================================================================="
echo "                         SEARCH COMPLETED"
echo "===================================================================="
echo ""
echo "Results have been saved to the 'output' folder"
echo "Check job_finder.log for detailed information"
echo ""
