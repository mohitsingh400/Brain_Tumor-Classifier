#!/usr/bin/env python
"""
Setup verification script for Brain Tumor AI Classifier
This script checks if all required dependencies are installed.
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("=" * 60)
    print("Python Environment Check")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path[:3]}...")
    print()

def check_django():
    """Check Django installation"""
    try:
        import django
        print("[OK] Django is installed")
        print(f"     Version: {django.get_version()}")
        print(f"     Location: {django.__file__}")
        return True
    except ImportError as e:
        print("[FAIL] Django is NOT installed")
        print(f"       Error: {e}")
        return False

def check_tensorflow():
    """Check TensorFlow installation"""
    try:
        import tensorflow as tf
        print("[OK] TensorFlow is installed")
        print(f"     Version: {tf.__version__}")
        return True
    except ImportError as e:
        print("[FAIL] TensorFlow is NOT installed")
        print(f"       Error: {e}")
        return False

def check_other_dependencies():
    """Check other important dependencies"""
    dependencies = {
        'PIL': 'Pillow',
        'numpy': 'numpy',
        'cv2': 'opencv-python',
        'sklearn': 'scikit-learn',
    }
    
    results = {}
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"[OK] {package} is installed")
            results[package] = True
        except ImportError:
            print(f"[FAIL] {package} is NOT installed")
            results[package] = False
    
    return results

def check_model_files():
    """Check if model files exist in the organized models/ directory"""
    print("\n" + "=" * 60)
    print("Model Files Check")
    print("=" * 60)
    
    # Get project root (parent of scripts directory)
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(scripts_dir)  # Go up one level to project root
    
    # Updated paths to check models/ directory first, then fallback locations
    models_dir = os.path.join(base_dir, 'models')
    model_files = {
        'CNN Model': [
            os.path.join(models_dir, 'brain_tumor_cnn.h5'),  # New organized location
            os.path.join(base_dir, 'brain_tumor_cnn.h5'),    # Fallback
            os.path.join(base_dir, 'src', 'brain_tumor_cnn.h5'),
        ],
        'VGG16 Model': [
            os.path.join(models_dir, 'brain_tumor_vgg16.h5'),  # New organized location
            os.path.join(base_dir, 'brain_tumor_vgg16.h5'),    # Fallback
            os.path.join(base_dir, 'src', 'brain_tumor_vgg16.h5'),
        ]
    }
    
    all_found = True
    for model_name, paths in model_files.items():
        found = False
        for path in paths:
            if os.path.exists(path):
                print(f"[OK] {model_name} found at: {path}")
                found = True
                break
        if not found:
            print(f"[FAIL] {model_name} NOT found")
            print(f"       Checked paths: {paths}")
            all_found = False
    
    return all_found

def main():
    """Run all checks"""
    print("\n" + "=" * 60)
    print("Brain Tumor AI Classifier - Setup Verification")
    print("=" * 60 + "\n")
    
    check_python_version()
    
    print("=" * 60)
    print("Dependencies Check")
    print("=" * 60)
    
    django_ok = check_django()
    tensorflow_ok = check_tensorflow()
    other_deps = check_other_dependencies()
    
    models_ok = check_model_files()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_ok = django_ok and tensorflow_ok and all(other_deps.values()) and models_ok
    
    if all_ok:
        print("[SUCCESS] All checks passed! You're ready to run the application.")
        print("\nTo start the server, run:")
        print("  python manage.py runserver")
    else:
        print("[ERROR] Some checks failed. Please install missing dependencies.")
        if not django_ok:
            print("\nTo install Django and all dependencies, run:")
            print("  python -m pip install -r requirements.txt")
    
    print("\n" + "=" * 60 + "\n")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())

