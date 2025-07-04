#!/usr/bin/env python3
"""
Simulate API response untuk debug
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import Config
from app.models import PropertiTanah, PropertiTanahBangunan
import json

# Create Flask app for database connection
app = Flask(__name__)
app.config.from_object(Config)

def simulate_api_response():
    with app.app_context():
        print("=== SIMULATING /api/admin/properties RESPONSE ===")
        
        # Get all properties like the API does
        tanah_properties = PropertiTanah.get_all()
        bangunan_properties = PropertiTanahBangunan.get_all()
        
        all_properties = []
        all_properties.extend([prop.to_dict() for prop in tanah_properties])
        all_properties.extend([prop.to_dict() for prop in bangunan_properties])
        
        # Sort by ID descending like API
        all_properties.sort(key=lambda x: x.get('id', 0), reverse=True)
        
        # Simulate pagination (first 10)
        total_items = len(all_properties)
        properties = all_properties[0:10]  # offset=0, limit=10
        
        response = {
            'properties': properties,
            'total': total_items,
            'page': 1,
            'per_page': 10,
            'total_pages': (total_items + 10 - 1) // 10
        }
        
        print(f"Total properties: {total_items}")
        print(f"Properties in page 1: {len(properties)}")
        print("\nProperties list:")
        
        for prop in properties:
            print(f"  - ID: {prop.get('id')}, Type: {prop.get('property_type')}, Title: {prop.get('title')}")
        
        print(f"\nFull API Response:")
        print(json.dumps(response, indent=2, default=str))

        # Test filter for tanah_bangunan only
        print("\n=== SIMULATING ?property_type=tanah_bangunan ===")
        bangunan_only = [prop.to_dict() for prop in bangunan_properties]
        
        response_tb = {
            'properties': bangunan_only,
            'total': len(bangunan_only),
            'page': 1,
            'per_page': 10,
            'total_pages': (len(bangunan_only) + 10 - 1) // 10
        }
        
        print(f"Tanah+Bangunan properties: {len(bangunan_only)}")
        for prop in bangunan_only:
            print(f"  - ID: {prop.get('id')}, Type: {prop.get('property_type')}, Title: {prop.get('title')}")

if __name__ == "__main__":
    simulate_api_response()
