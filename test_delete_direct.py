#!/usr/bin/env python3
"""
Direct database test untuk memastikan delete function bekerja
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import Config
from app.models import PropertiTanah, PropertiTanahBangunan, User

# Create Flask app for database connection
app = Flask(__name__)
app.config.from_object(Config)

def test_delete_directly():
    with app.app_context():
        print("=== BEFORE DELETE ===")
        tanah_properties = PropertiTanah.get_all()
        bangunan_properties = PropertiTanahBangunan.get_all()
        
        print(f"Properti Tanah: {len(tanah_properties)}")
        for prop in tanah_properties:
            print(f"  - ID: {prop.id}, Title: {prop.title}")
        
        print(f"Properti Tanah+Bangunan: {len(bangunan_properties)}")
        for prop in bangunan_properties:
            print(f"  - ID: {prop.id}, Title: {prop.title}")
        
        # Test delete a property directly
        if len(bangunan_properties) > 0:
            prop_to_delete = bangunan_properties[0]
            print(f"\nTesting delete on: ID={prop_to_delete.id}, Title={prop_to_delete.title}")
            
            # Test delete method directly
            result = prop_to_delete.delete()
            print(f"Delete result: {result}")
            
            print("\n=== AFTER DELETE ===")
            tanah_properties = PropertiTanah.get_all()
            bangunan_properties = PropertiTanahBangunan.get_all()
            
            print(f"Properti Tanah: {len(tanah_properties)}")
            for prop in tanah_properties:
                print(f"  - ID: {prop.id}, Title: {prop.title}")
            
            print(f"Properti Tanah+Bangunan: {len(bangunan_properties)}")
            for prop in bangunan_properties:
                print(f"  - ID: {prop.id}, Title: {prop.title}")
        
        # Check if admin user exists
        print(f"\n=== CHECKING ADMIN USER ===")
        admin_user = User.find_by_email('admin@telkom.com')
        if admin_user:
            print(f"Admin user found: ID={admin_user.id}, Name={admin_user.name}, Role={admin_user.role}")
            
            # Test password
            test_password = admin_user.check_password('admin123')
            print(f"Password check for 'admin123': {test_password}")
        else:
            print("Admin user not found!")

if __name__ == "__main__":
    test_delete_directly()
