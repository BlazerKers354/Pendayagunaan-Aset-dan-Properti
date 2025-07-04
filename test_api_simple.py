#!/usr/bin/env python3
"""
Test API langsung saat server sudah berjalan
"""

import requests
import json

def test_api_simple():
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # Login
    print("Testing login...")
    login_data = {"email": "admin@telkom.com", "password": "admin123"}
    login_response = session.post(f"{base_url}/login", data=login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code != 200:
        print("LOGIN FAILED!")
        return
    
    # Test admin properties endpoint
    print("\nTesting /api/admin/properties...")
    response = session.get(f"{base_url}/api/admin/properties")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        properties = data.get('properties', [])
        print(f"Total properties: {data.get('total', 0)}")
        print(f"Properties in response: {len(properties)}")
        
        for prop in properties:
            print(f"  - ID: {prop.get('id')}, Type: {prop.get('property_type')}, Title: {prop.get('title')}")
    else:
        print(f"Error: {response.text}")

    # Test tanah_bangunan filter
    print("\nTesting /api/admin/properties?property_type=tanah_bangunan...")
    response = session.get(f"{base_url}/api/admin/properties?property_type=tanah_bangunan")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        properties = data.get('properties', [])
        print(f"Tanah+Bangunan properties: {len(properties)}")
        
        for prop in properties:
            print(f"  - ID: {prop.get('id')}, Type: {prop.get('property_type')}, Title: {prop.get('title')}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_api_simple()
