#!/bin/bash
# Quick start script for SafeEye backend

echo "Starting SafeEye Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "MONGODB_URL=mongodb://localhost:27017" > .env
    echo "DATABASE_NAME=safeye" >> .env
    echo "Please update .env with your MongoDB connection string"
fi

# Create directories
mkdir -p uploads processed

# Start server
echo "Starting FastAPI server..."
uvicorn main:app --reload --port 8000

