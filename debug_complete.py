#!/usr/bin/env python3
"""
Script debug lengkap untuk troubleshoot masalah properti tanah+bangunan
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

def check_database():
    print("=== CHECKING DATABASE ===")
    with app.app_context():
        # Check tanah properties
        tanah_properties = PropertiTanah.get_all()
        print(f"Properti Tanah: {len(tanah_properties)} records")
        for prop in tanah_properties[:3]:  # Show first 3
            print(f"  - ID: {prop.id}, Title: {prop.title}")
        
        # Check tanah+bangunan properties  
        bangunan_properties = PropertiTanahBangunan.get_all()
        print(f"Properti Tanah+Bangunan: {len(bangunan_properties)} records")
        for prop in bangunan_properties[:3]:  # Show first 3
            print(f"  - ID: {prop.id}, Title: {prop.title}")
        
        print(f"Total: {len(tanah_properties) + len(bangunan_properties)} properties")

def test_api():
    print("\n=== TESTING API ===")
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # Login
    login_data = {"email": "admin@telkom.com", "password": "admin123"}
    login_response = session.post(f"{base_url}/login", data=login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("LOGIN FAILED!")
        return
    
    # Test admin properties endpoint
    endpoints = [
        ("/api/admin/properties", "All properties (admin)"),
        ("/api/admin/properties?property_type=tanah", "Tanah only (admin)"),
        ("/api/admin/properties?property_type=tanah_bangunan", "Tanah+Bangunan only (admin)"),
        ("/api/properties", "All properties (public)"),
    ]
    
    for endpoint, description in endpoints:
        print(f"\nTesting {endpoint} - {description}")
        response = session.get(f"{base_url}{endpoint}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                properties = data.get('properties', [])
                print(f"Total properties: {data.get('total', 0)}")
                print(f"Properties in response: {len(properties)}")
                
                # Show property types
                type_counts = {}
                for prop in properties:
                    prop_type = prop.get('property_type', 'unknown')
                    type_counts[prop_type] = type_counts.get(prop_type, 0) + 1
                
                for prop_type, count in type_counts.items():
                    print(f"  - {prop_type}: {count} properties")
                    
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                print(f"Response: {response.text}")
        else:
            print(f"Error response: {response.text}")

def test_create_property():
    print("\n=== TESTING CREATE PROPERTY ===")
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # Login
    login_data = {"email": "admin@telkom.com", "password": "admin123"}
    login_response = session.post(f"{base_url}/login", data=login_data)
    
    if login_response.status_code != 200:
        print("LOGIN FAILED!")
        return
    
    # Create tanah+bangunan property
    property_data = {
        "property_type": "tanah_bangunan",
        "title": "Test Properti Tanah+Bangunan",
        "location": "Surabaya Test",
        "price": 1500000000,
        "land_area": 150.0,
        "building_area": 120.0,
        "bedrooms": 3,
        "bathrooms": 2,
        "floors": 2,
        "certificate": "SHM",
        "condition_property": "Baik",
        "facing": "Utara",
        "water_source": "PDAM",
        "internet": "Ya",
        "hook": "Tidak",
        "power": 2200,
        "description": "Test property for debugging",
        "status": "aktif"
    }
    
    print("Creating new tanah+bangunan property...")
    response = session.post(
        f"{base_url}/api/admin/property",
        headers={'Content-Type': 'application/json'},
        data=json.dumps(property_data)
    )
    
    print(f"Create response status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('message')}")
        print(f"New property ID: {result.get('property', {}).get('id')}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    check_database()
    test_api()
    test_create_property()
    
    # Check database again after create
    print("\n=== AFTER CREATE TEST ===")
    check_database()
