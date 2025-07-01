import pandas as pd
import os
import numpy as np
from typing import List, Dict, Optional, Tuple

class AssetDataProcessor:
    def __init__(self, csv_path: str = None):
        """Initialize the processor with CSV data"""
        if csv_path is None:
            csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'dataset_aset.csv')
        
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and clean the CSV data"""
        try:
            # Read CSV with semicolon separator
            self.df = pd.read_csv(self.csv_path, sep=';', encoding='utf-8')
            
            # Clean column names (remove spaces)
            self.df.columns = self.df.columns.str.strip()
            
            # Clean price column - remove spaces and convert to numeric
            self.df['Price'] = self.df['Price'].astype(str).str.replace('.', '').str.replace(' ', '').str.replace(',', '')
            self.df['Price'] = pd.to_numeric(self.df['Price'], errors='coerce')
            
            # Clean numeric columns
            numeric_columns = ['Kamar Tidur', 'Kamar Mandi', 'Luas Tanah', 'Luas Bangunan', 'Daya Listrik', 'Jumlah Lantai']
            for col in numeric_columns:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
            # Clean string columns
            string_columns = ['Kecamatan', 'Sertifikat', 'Ruang Makan', 'Ruang Tamu', 'Kondisi Perabotan', 
                            'Hadap', 'Terjangkau Internet', 'Lebar Jalan', 'Sumber Air', 'Hook', 'Kondisi Properti']
            for col in string_columns:
                if col in self.df.columns:
                    self.df[col] = self.df[col].astype(str).str.strip()
                    # Replace 'nan' with empty string for better handling
                    self.df[col] = self.df[col].replace('nan', '')
            
            # Remove rows with invalid prices
            self.df = self.df.dropna(subset=['Price'])
            self.df = self.df[self.df['Price'] > 0]
            
            print(f"Loaded {len(self.df)} records from dataset")
            
        except Exception as e:
            print(f"Error loading data: {e}")
            # Create dummy data if CSV fails to load
            self.create_dummy_data()
    
    def create_dummy_data(self):
        """Create dummy data if CSV loading fails"""
        dummy_data = {
            'Kecamatan': ['wonokromo', 'rungkut', 'semampir', 'pakal', 'gayungan'] * 100,
            'Price': [600000000, 650000000, 700000000, 750000000, 800000000] * 100,
            'Kamar Tidur': [2, 3, 3, 4, 2] * 100,
            'Kamar Mandi': [1, 2, 2, 2, 1] * 100,
            'Luas Tanah': [60, 72, 80, 90, 65] * 100,
            'Luas Bangunan': [50, 65, 70, 80, 55] * 100,
            'Sertifikat': ['SHM - Sertifikat Hak Milik'] * 500,
            'Kondisi Properti': ['Baru', 'Bagus', 'Sudah Renovasi'] * 167
        }
        self.df = pd.DataFrame(dummy_data)
    
    def get_all_properties(self, limit: int = None) -> List[Dict]:
        """Get all properties as list of dictionaries"""
        if self.df is None or self.df.empty:
            return []
        
        df_subset = self.df.head(limit) if limit else self.df
        
        properties = []
        for _, row in df_subset.iterrows():
            prop = {
                'id': int(row.name),
                'title': f"Rumah {row['Kecamatan'].title()} - {row['Kamar Tidur']}KT/{row['Kamar Mandi']}KM",
                'location': row['Kecamatan'].title(),
                'price': int(row['Price']) if pd.notna(row['Price']) else 0,
                'bedrooms': int(row['Kamar Tidur']) if pd.notna(row['Kamar Tidur']) else 0,
                'bathrooms': int(row['Kamar Mandi']) if pd.notna(row['Kamar Mandi']) else 0,
                'land_area': int(row['Luas Tanah']) if pd.notna(row['Luas Tanah']) else 0,
                'building_area': int(row['Luas Bangunan']) if pd.notna(row['Luas Bangunan']) else 0,
                'certificate': row['Sertifikat'] if pd.notna(row['Sertifikat']) else 'N/A',
                'power': int(row['Daya Listrik']) if pd.notna(row['Daya Listrik']) else 0,
                'floors': int(row['Jumlah Lantai']) if pd.notna(row['Jumlah Lantai']) else 1,
                'condition': row['Kondisi Properti'] if pd.notna(row['Kondisi Properti']) else 'N/A',
                'furnished': row['Kondisi Perabotan'] if pd.notna(row['Kondisi Perabotan']) else 'N/A',
                'facing': row['Hadap'] if pd.notna(row['Hadap']) else 'N/A',
                'internet': row['Terjangkau Internet'] if pd.notna(row['Terjangkau Internet']) else 'N/A',
                'road_width': row['Lebar Jalan'] if pd.notna(row['Lebar Jalan']) else 'N/A',
                'water_source': row['Sumber Air'] if pd.notna(row['Sumber Air']) else 'N/A',
                'hook': row['Hook'] if pd.notna(row['Hook']) else 'N/A',
                'type': 'Rumah',
                'transaction_type': 'Jual'  # Assuming all are for sale based on the price data
            }
            
            # Calculate price per m2
            if prop['land_area'] > 0:
                prop['price_per_m2'] = prop['price'] // prop['land_area']
            else:
                prop['price_per_m2'] = 0
            
            properties.append(prop)
        
        return properties
    
    def get_filtered_properties(self, filters: Dict = None, limit: int = None) -> List[Dict]:
        """Get filtered properties based on criteria"""
        if self.df is None or self.df.empty:
            return []
        
        filtered_df = self.df.copy()
        
        if filters:
            # Filter by location/kecamatan
            if filters.get('location'):
                filtered_df = filtered_df[
                    filtered_df['Kecamatan'].str.lower().str.contains(filters['location'].lower(), na=False)
                ]
            
            # Filter by price range
            if filters.get('min_price'):
                filtered_df = filtered_df[filtered_df['Price'] >= filters['min_price']]
            if filters.get('max_price'):
                filtered_df = filtered_df[filtered_df['Price'] <= filters['max_price']]
            
            # Filter by bedrooms
            if filters.get('bedrooms'):
                filtered_df = filtered_df[filtered_df['Kamar Tidur'] == filters['bedrooms']]
            
            # Filter by bathrooms
            if filters.get('bathrooms'):
                filtered_df = filtered_df[filtered_df['Kamar Mandi'] == filters['bathrooms']]
            
            # Filter by land area
            if filters.get('min_land_area'):
                filtered_df = filtered_df[filtered_df['Luas Tanah'] >= filters['min_land_area']]
            if filters.get('max_land_area'):
                filtered_df = filtered_df[filtered_df['Luas Tanah'] <= filters['max_land_area']]
            
            # Filter by condition
            if filters.get('condition'):
                filtered_df = filtered_df[
                    filtered_df['Kondisi Properti'].str.lower().str.contains(filters['condition'].lower(), na=False)
                ]
        
        # Convert to list format
        properties = []
        df_subset = filtered_df.head(limit) if limit else filtered_df
        
        for _, row in df_subset.iterrows():
            prop = {
                'id': int(row.name),
                'title': f"Rumah {row['Kecamatan'].title()} - {row['Kamar Tidur']}KT/{row['Kamar Mandi']}KM",
                'location': row['Kecamatan'].title(),
                'price': int(row['Price']) if pd.notna(row['Price']) else 0,
                'bedrooms': int(row['Kamar Tidur']) if pd.notna(row['Kamar Tidur']) else 0,
                'bathrooms': int(row['Kamar Mandi']) if pd.notna(row['Kamar Mandi']) else 0,
                'land_area': int(row['Luas Tanah']) if pd.notna(row['Luas Tanah']) else 0,
                'building_area': int(row['Luas Bangunan']) if pd.notna(row['Luas Bangunan']) else 0,
                'certificate': row['Sertifikat'] if pd.notna(row['Sertifikat']) else 'N/A',
                'power': int(row['Daya Listrik']) if pd.notna(row['Daya Listrik']) else 0,
                'floors': int(row['Jumlah Lantai']) if pd.notna(row['Jumlah Lantai']) else 1,
                'condition': row['Kondisi Properti'] if pd.notna(row['Kondisi Properti']) else 'N/A',
                'furnished': row['Kondisi Perabotan'] if pd.notna(row['Kondisi Perabotan']) else 'N/A',
                'facing': row['Hadap'] if pd.notna(row['Hadap']) else 'N/A',
                'internet': row['Terjangkau Internet'] if pd.notna(row['Terjangkau Internet']) else 'N/A',
                'road_width': row['Lebar Jalan'] if pd.notna(row['Lebar Jalan']) else 'N/A',
                'water_source': row['Sumber Air'] if pd.notna(row['Sumber Air']) else 'N/A',
                'hook': row['Hook'] if pd.notna(row['Hook']) else 'N/A',
                'type': 'Rumah',
                'transaction_type': 'Jual'
            }
            
            # Calculate price per m2
            if prop['land_area'] > 0:
                prop['price_per_m2'] = prop['price'] // prop['land_area']
            else:
                prop['price_per_m2'] = 0
            
            properties.append(prop)
        
        return properties
    
    def get_statistics(self) -> Dict:
        """Get basic statistics from the dataset"""
        if self.df is None or self.df.empty:
            return {}
        
        stats = {
            'total_properties': len(self.df),
            'avg_price': int(self.df['Price'].mean()),
            'min_price': int(self.df['Price'].min()),
            'max_price': int(self.df['Price'].max()),
            'avg_land_area': int(self.df['Luas Tanah'].mean()) if 'Luas Tanah' in self.df.columns else 0,
            'avg_building_area': int(self.df['Luas Bangunan'].mean()) if 'Luas Bangunan' in self.df.columns else 0,
            'locations': list(self.df['Kecamatan'].str.title().unique()),
            'conditions': [cond for cond in self.df['Kondisi Properti'].dropna().unique() if cond and cond != ''],
            'certificates': [cert for cert in self.df['Sertifikat'].dropna().unique() if cert and cert != '']
        }
        
        return stats
    
    def get_price_by_location(self) -> Dict:
        """Get average prices by location"""
        if self.df is None or self.df.empty:
            return {}
        
        location_prices = self.df.groupby('Kecamatan')['Price'].agg(['mean', 'count']).round(0)
        location_prices.columns = ['avg_price', 'count']
        
        result = {}
        for location, data in location_prices.iterrows():
            result[location.title()] = {
                'avg_price': int(data['avg_price']),
                'count': int(data['count'])
            }
        
        return result
    
    def get_property_by_id(self, property_id: int) -> Optional[Dict]:
        """Get specific property by ID"""
        if self.df is None or self.df.empty:
            return None
        
        try:
            row = self.df.iloc[property_id]
            prop = {
                'id': property_id,
                'title': f"Rumah {row['Kecamatan'].title()} - {row['Kamar Tidur']}KT/{row['Kamar Mandi']}KM",
                'location': row['Kecamatan'].title(),
                'price': int(row['Price']) if pd.notna(row['Price']) else 0,
                'bedrooms': int(row['Kamar Tidur']) if pd.notna(row['Kamar Tidur']) else 0,
                'bathrooms': int(row['Kamar Mandi']) if pd.notna(row['Kamar Mandi']) else 0,
                'land_area': int(row['Luas Tanah']) if pd.notna(row['Luas Tanah']) else 0,
                'building_area': int(row['Luas Bangunan']) if pd.notna(row['Luas Bangunan']) else 0,
                'certificate': row['Sertifikat'] if pd.notna(row['Sertifikat']) else 'N/A',
                'power': int(row['Daya Listrik']) if pd.notna(row['Daya Listrik']) else 0,
                'floors': int(row['Jumlah Lantai']) if pd.notna(row['Jumlah Lantai']) else 1,
                'condition': row['Kondisi Properti'] if pd.notna(row['Kondisi Properti']) else 'N/A',
                'furnished': row['Kondisi Perabotan'] if pd.notna(row['Kondisi Perabotan']) else 'N/A',
                'facing': row['Hadap'] if pd.notna(row['Hadap']) else 'N/A',
                'internet': row['Terjangkau Internet'] if pd.notna(row['Terjangkau Internet']) else 'N/A',
                'road_width': row['Lebar Jalan'] if pd.notna(row['Lebar Jalan']) else 'N/A',
                'water_source': row['Sumber Air'] if pd.notna(row['Sumber Air']) else 'N/A',
                'hook': row['Hook'] if pd.notna(row['Hook']) else 'N/A',
                'dining_room': row['Ruang Makan'] if pd.notna(row['Ruang Makan']) else 'N/A',
                'living_room': row['Ruang Tamu'] if pd.notna(row['Ruang Tamu']) else 'N/A',
                'type': 'Rumah',
                'transaction_type': 'Jual'
            }
            
            # Calculate price per m2
            if prop['land_area'] > 0:
                prop['price_per_m2'] = prop['price'] // prop['land_area']
            else:
                prop['price_per_m2'] = 0
            
            return prop
            
        except (IndexError, KeyError):
            return None
