#!/usr/bin/env python3
"""
Create admin user for testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import Config
from app.models import User

# Create Flask app for database connection
app = Flask(__name__)
app.config.from_object(Config)

def create_admin_user():
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.find_by_email('admin@telkom.com')
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Create new admin user
        admin_user = User(
            name='Admin Telkom',
            email='admin@telkom.com',
            password='admin123',  # Will be hashed automatically
            role='admin'
        )
        
        if admin_user.save():
            print("Admin user created successfully!")
            print(f"Email: admin@telkom.com")
            print(f"Password: admin123")
        else:
            print("Failed to create admin user")

if __name__ == "__main__":
    create_admin_user()
