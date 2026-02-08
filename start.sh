#!/bin/bash

# Truth-in-Taxation Server Startup Script

echo "=========================================="
echo "Truth-in-Taxation Forms Portal"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python version: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo ""
echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Start the server
echo ""
echo "=========================================="
echo "Starting Flask server..."
echo "=========================================="
echo ""
echo "Server will be available at:"
echo "  → http://localhost:5000"
echo ""
echo "Open truth-in-taxation-complete.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 server.py
