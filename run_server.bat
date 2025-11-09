@echo off
echo Starting Brain Tumor AI Classifier Web Application...
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not found in PATH!
    echo Please make sure Python is installed and added to your PATH.
    pause
    exit /b 1
)
echo.

echo Checking Django installation...
python -c "import django; print('Django version:', django.get_version())" 2>nul
if errorlevel 1 (
    echo Django is not installed. Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)
echo.

echo Creating necessary directories...
if not exist "media\predictions" mkdir "media\predictions"
if not exist "staticfiles" mkdir "staticfiles"
echo.

echo Running migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo Starting Django development server...
echo.
echo ========================================
echo   Server starting at http://127.0.0.1:8000/
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver

pause

