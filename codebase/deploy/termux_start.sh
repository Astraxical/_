#!/bin/bash

# Termux startup script for Multi-House Application

# Set environment variables
export DEBUG=True
export PORT=8000
export DATABASE_URL="sqlite:///./data/app.db"

# Create necessary directories if they don't exist
mkdir -p data
mkdir -p logs

# Initialize the database
echo "Initializing database..."
python init_db.py

# Start the application with uvicorn
echo "Starting Multi-House Application..."
uvicorn main:app --host 0.0.0.0 --port $PORT --reload