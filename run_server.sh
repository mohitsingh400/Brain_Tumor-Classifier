#!/bin/bash

echo "Starting Brain Tumor AI Classifier Web Application..."
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

echo "Checking Python installation..."
python --version
echo ""

echo "Creating necessary directories..."
mkdir -p media/predictions
mkdir -p staticfiles
echo ""

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate
echo ""

echo "Starting Django development server..."
echo "Open http://127.0.0.1:8000/ in your browser"
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver

