#!/usr/bin/env python3
"""
Test delete functionality
"""

import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import Config
from app.models import PropertiTanah, PropertiTanahBangunan

# Create Flask app for database connection
app = Flask(__name__)
app.config.from_object(Config)

def test_delete_api():
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # Login
    print("=== LOGIN ===")
    login_data = {"email": "admin@telkom.com", "password": "admin123"}
    login_response = session.post(f"{base_url}/login", data=login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("LOGIN FAILED!")
        return
    
    # Get current properties first
    print("\n=== GET CURRENT PROPERTIES ===")
    response = session.get(f"{base_url}/api/admin/properties")
    if response.status_code == 200:
        data = response.json()
        properties = data.get('properties', [])
        print(f"Current properties: {len(properties)}")
        
        for prop in properties:
            print(f"  - ID: {prop.get('id')}, Type: {prop.get('property_type')}, Title: {prop.get('title')}")
        
        if len(properties) > 0:
            # Try to delete the first property
            prop_to_delete = properties[0]
            prop_id = prop_to_delete.get('id')
            prop_type = prop_to_delete.get('property_type')
            
            print(f"\n=== TESTING DELETE ===")
            print(f"Attempting to delete: ID={prop_id}, Type={prop_type}, Title={prop_to_delete.get('title')}")
            
            delete_response = session.delete(f"{base_url}/api/admin/property/{prop_type}/{prop_id}")
            print(f"Delete response status: {delete_response.status_code}")
            print(f"Delete response: {delete_response.text}")
            
            # Get properties again to verify deletion
            print(f"\n=== VERIFY DELETION ===")
            response = session.get(f"{base_url}/api/admin/properties")
            if response.status_code == 200:
                data = response.json()
                new_properties = data.get('properties', [])
                print(f"Properties after deletion: {len(new_properties)}")
                
                deleted = not any(p.get('id') == prop_id and p.get('property_type') == prop_type for p in new_properties)
                print(f"Property successfully deleted: {deleted}")
            else:
                print("Failed to get properties after deletion")
        else:
            print("No properties to delete")
    else:
        print("Failed to get current properties")

def check_database_before_after():
    print("\n=== DATABASE CHECK ===")
    with app.app_context():
        tanah_properties = PropertiTanah.get_all()
        bangunan_properties = PropertiTanahBangunan.get_all()
        
        print(f"Properti Tanah: {len(tanah_properties)}")
        for prop in tanah_properties:
            print(f"  - ID: {prop.id}, Title: {prop.title}")
            
        print(f"Properti Tanah+Bangunan: {len(bangunan_properties)}")
        for prop in bangunan_properties:
            print(f"  - ID: {prop.id}, Title: {prop.title}")

if __name__ == "__main__":
    check_database_before_after()
    test_delete_api()
    check_database_before_after()
