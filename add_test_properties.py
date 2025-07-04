#!/usr/bin/env python3
"""
Add more test properties for delete testing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from config import Config
from app.models import PropertiTanah, PropertiTanahBangunan

# Create Flask app for database connection
app = Flask(__name__)
app.config.from_object(Config)

def add_test_properties():
    with app.app_context():
        # Add another tanah property
        tanah_prop = PropertiTanah(
            title='Test Tanah Kosong 2',
            location='Surabaya Barat',
            price=750000000,
            land_area=200.0,
            certificate='SHM',
            facing='selatan',
            water_source='PDAM',
            internet='Ya',
            hook='Ya',
            power=1300,
            road_width='8 meter',
            description='Test tanah kosong kedua',
            status='aktif',
            created_by=1
        )
        
        if tanah_prop.save():
            print(f"Added tanah property: {tanah_prop.title} (ID: {tanah_prop.id})")
        
        # Add another bangunan property
        bangunan_prop = PropertiTanahBangunan(
            title='Test Rumah Minimalis',
            location='Surabaya Timur',
            price=1800000000,
            land_area=150.0,
            building_area=100.0,
            bedrooms=3,
            bathrooms=2,
            floors=2,
            certificate='SHM',
            condition_property='baik',
            facing='timur',
            water_source='PDAM',
            internet='Ya',
            hook='Ya',
            power=2200,
            dining_room='1',
            living_room='1',
            road_width='6 meter',
            furnished='Unfurnished',
            description='Test rumah minimalis untuk testing delete',
            status='aktif',
            created_by=1
        )
        
        if bangunan_prop.save():
            print(f"Added bangunan property: {bangunan_prop.title} (ID: {bangunan_prop.id})")
        
        # Show all properties
        print("\n=== ALL PROPERTIES ===")
        tanah_properties = PropertiTanah.get_all()
        bangunan_properties = PropertiTanahBangunan.get_all()
        
        print(f"Properti Tanah: {len(tanah_properties)}")
        for prop in tanah_properties:
            print(f"  - ID: {prop.id}, Title: {prop.title}")
        
        print(f"Properti Tanah+Bangunan: {len(bangunan_properties)}")
        for prop in bangunan_properties:
            print(f"  - ID: {prop.id}, Title: {prop.title}")

if __name__ == "__main__":
    add_test_properties()
