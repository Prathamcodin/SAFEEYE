@echo off
REM Quick start script for SafeEye backend (Windows)

echo Starting SafeEye Backend...

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    echo MONGODB_URL=mongodb://localhost:27017 > .env
    echo DATABASE_NAME=safeye >> .env
    echo Please update .env with your MongoDB connection string
)

REM Create directories
if not exist "uploads" mkdir uploads
if not exist "processed" mkdir processed

REM Start server
echo Starting FastAPI server...
uvicorn main:app --reload --port 8000

