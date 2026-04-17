#!/bin/bash
# CloseZap AI - Unix/Linux/Mac Startup Script

echo "================================================"
echo "CloseZap AI - Starting Development Server"
echo "================================================"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Change to script directory
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Create .env if not exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo "Please edit .env with your credentials!"
    fi
fi

# Run server
echo ""
echo "================================================"
echo "Server starting at http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "================================================"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000