#!/usr/bin/env python3
"""
Script untuk mengecek data di tabel properti_tanah dan properti_tanah_bangunan
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

def check_data():
    with app.app_context():
        print("=== Checking PropertiTanah data ===")
        tanah_properties = PropertiTanah.get_all()
        print(f"Total properti tanah: {len(tanah_properties)}")
        for prop in tanah_properties:
            print(f"- ID: {prop.id}, Title: {prop.title}, Location: {prop.location}")
        
        print("\n=== Checking PropertiTanahBangunan data ===")
        bangunan_properties = PropertiTanahBangunan.get_all()
        print(f"Total properti tanah+bangunan: {len(bangunan_properties)}")
        for prop in bangunan_properties:
            print(f"- ID: {prop.id}, Title: {prop.title}, Location: {prop.location}")
        
        print(f"\nTotal semua properti: {len(tanah_properties) + len(bangunan_properties)}")

if __name__ == "__main__":
    check_data()
