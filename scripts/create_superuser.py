#!/usr/bin/env python
"""
Django Superuser Creation Script
This script creates a Django superuser for accessing the admin panel.
Usage: python scripts/create_superuser.py
Or run from project root: python scripts/create_superuser.py
"""

import os
import sys
import django

# Add project root to Python path
scripts_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(scripts_dir)
sys.path.insert(0, base_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brain_tumor_web.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser(username='admin', email='admin@example.com', password='admin123'):
    """Create a superuser with the given credentials"""
    try:
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            print(f"User '{username}' already exists!")
            response = input("Do you want to change the password? (y/n): ")
            if response.lower() == 'y':
                user = User.objects.get(username=username)
                user.set_password(password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                print(f"Password updated for user '{username}'")
            return
        
        # Create new superuser
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("=" * 60)
        print("Superuser created successfully!")
        print("=" * 60)
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("=" * 60)
        print("\nYou can now login at: http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"Error creating superuser: {e}")
        sys.exit(1)

if __name__ == '__main__':
    print("Django Superuser Creation")
    print("=" * 60)
    
    # Get user input
    username = input("Enter username (default: admin): ").strip() or 'admin'
    email = input("Enter email (default: admin@example.com): ").strip() or 'admin@example.com'
    password = input("Enter password (default: admin123): ").strip() or 'admin123'
    
    # Confirm password
    password_confirm = input("Confirm password: ").strip()
    if password != password_confirm:
        print("Passwords do not match!")
        sys.exit(1)
    
    create_superuser(username, email, password)


