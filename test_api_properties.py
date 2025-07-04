#!/usr/bin/env python3
"""
Script untuk test API endpoint /api/properties
"""

import requests
import json

def test_api_properties():
    base_url = "http://localhost:5000"
    
    # Login terlebih dahulu untuk mendapatkan session
    login_data = {
        "email": "admin@telkom.com",
        "password": "admin123"
    }
    
    session = requests.Session()
    
    # Login
    login_response = session.post(f"{base_url}/login", data=login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        # Test API properties tanpa filter
        print("\n=== Testing /api/properties (all types) ===")
        response = session.get(f"{base_url}/api/properties")
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total properties: {data.get('total', 0)}")
            print(f"Properties in current page: {len(data.get('properties', []))}")
            for prop in data.get('properties', []):
                print(f"- ID: {prop.get('id')}, Type: {prop.get('property_type')}, Title: {prop.get('title')}")
        else:
            print(f"Error: {response.text}")
        
        # Test API properties tanah only
        print("\n=== Testing /api/properties?property_type=tanah ===")
        response = session.get(f"{base_url}/api/properties?property_type=tanah")
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total tanah properties: {data.get('total', 0)}")
            for prop in data.get('properties', []):
                print(f"- ID: {prop.get('id')}, Type: {prop.get('property_type')}, Title: {prop.get('title')}")
        else:
            print(f"Error: {response.text}")
        
        # Test API properties tanah_bangunan only
        print("\n=== Testing /api/properties?property_type=tanah_bangunan ===")
        response = session.get(f"{base_url}/api/properties?property_type=tanah_bangunan")
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total tanah+bangunan properties: {data.get('total', 0)}")
            for prop in data.get('properties', []):
                print(f"- ID: {prop.get('id')}, Type: {prop.get('property_type')}, Title: {prop.get('title')}")
        else:
            print(f"Error: {response.text}")
    else:
        print("Failed to login")

if __name__ == "__main__":
    test_api_properties()
