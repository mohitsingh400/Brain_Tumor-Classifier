# Troubleshooting Guide

## Issue: "ModuleNotFoundError: No module named 'django'"

This error occurs when Python cannot find Django. Here are several solutions:

### Solution 1: Verify Python Installation

Run this command to check if Django is accessible:
```bash
python -c "import django; print(django.get_version())"
```

If this works, the issue is with how you're running `manage.py`.

### Solution 2: Use the Correct Python Interpreter

Your IDE or terminal might be using a different Python interpreter. 

**In VS Code/Cursor:**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Python: Select Interpreter"
3. Choose the Python interpreter that has Django installed

**Check which Python is being used:**
```bash
where python
# or on Linux/Mac:
which python
```

### Solution 3: Install Dependencies Again

If Django is missing, install it:
```bash
cd "I:\research project\brain_tumor"
python -m pip install -r requirements.txt
```

### Solution 4: Use Virtual Environment (Recommended)

If you have a virtual environment (`myenv`), activate it first:

**Windows:**
```bash
cd "I:\research project"
.\myenv\Scripts\activate
cd brain_tumor
python manage.py runserver
```

**Linux/Mac:**
```bash
cd "I:\research project"
source myenv/bin/activate
cd brain_tumor
python manage.py runserver
```

### Solution 5: Run the Setup Check Script

Run the verification script:
```bash
python check_setup.py
```

This will tell you exactly what's missing.

### Solution 6: Use the Batch File

On Windows, use the provided batch file which handles setup automatically:
```bash
run_server.bat
```

## Issue: "Model file not found"

If you get errors about missing model files:

1. **Check if model files exist:**
   - `brain_tumor_cnn.h5` (in root directory)
   - `brain_tumor_vgg16.h5` (in root directory)
   - Or in `src/` folder

2. **If models are missing:**
   - Train the models first using `src/train.py`
   - Or download pre-trained models if available

## Issue: Static Files Not Loading

If CSS/JS files don't load:

1. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Check DEBUG setting:**
   - Make sure `DEBUG = True` in `brain_tumor_web/settings.py` for development

## Issue: Database Errors

If you get database-related errors:

1. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Delete and recreate database (if needed):**
   ```bash
   del db.sqlite3
   python manage.py migrate
   ```

## Issue: Port Already in Use

If port 8000 is already in use:

1. **Use a different port:**
   ```bash
   python manage.py runserver 8001
   ```

2. **Or find and kill the process using port 8000**

## Getting Help

If none of these solutions work:

1. Run `python check_setup.py` and share the output
2. Check the error message carefully
3. Verify your Python version: `python --version` (should be 3.8+)
4. Make sure you're in the correct directory: `I:\research project\brain_tumor`

## Quick Fix Command

Try this all-in-one command:
```bash
cd "I:\research project\brain_tumor" && python -m pip install -r requirements.txt && python manage.py migrate && python manage.py runserver
```


