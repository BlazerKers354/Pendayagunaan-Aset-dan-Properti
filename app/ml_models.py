"""
Modul Machine Learning untuk Prediksi Harga Properti
Menggunakan XGBoost, Random Forest, dan CatBoost
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
from catboost import CatBoostRegressor
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

class PropertyPricePredictor:
    def __init__(self):
        self.models = {}
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.target_column = 'NJOP_Rp_per_m2'
        
    def load_data(self, file_path):
        """Load dan preprocessing data"""
        try:
            # Load data
            df = pd.read_csv(file_path)
            
            # Clean data
            df = self._clean_data(df)
            
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def _clean_data(self, df):
        """Bersihkan dan preprocessing data"""
        print(f"📊 Original data shape: {df.shape}")
        print(f"📊 Columns: {list(df.columns)}")
        
        # Check if target column exists
        if self.target_column not in df.columns:
            print(f"❌ Target column '{self.target_column}' not found!")
            return df
        
        # Remove missing values in target column
        initial_count = len(df)
        df = df.dropna(subset=[self.target_column])
        print(f"📊 After removing missing target values: {len(df)} (removed {initial_count - len(df)})")
        
        # Remove rows where NJOP is 0 or negative
        df = df[df[self.target_column] > 0]
        print(f"📊 After removing zero/negative prices: {len(df)}")
        
        if len(df) == 0:
            print("❌ No valid data remaining after cleaning!")
            return df
        
        # Clean column names - remove leading/trailing spaces
        df.columns = df.columns.str.strip()
        
        # For building dataset, add default coordinates (Surabaya)
        df['Latitude'] = -7.2575 + np.random.normal(0, 0.1, len(df))  # Add some variation
        df['Longitude'] = 112.7521 + np.random.normal(0, 0.1, len(df))  # Add some variation
        
        # Create luas kategori based on available luas column
        if 'Luas Tanah' in df.columns:
            luas_col = 'Luas Tanah'
        elif 'Luas_m2' in df.columns:
            luas_col = 'Luas_m2'
        else:
            # Create a default luas column
            df['Luas_Tanah'] = 1000
            luas_col = 'Luas_Tanah'
        
        # Ensure luas column is numeric
        df[luas_col] = pd.to_numeric(df[luas_col], errors='coerce')
        df = df.dropna(subset=[luas_col])
        df = df[df[luas_col] > 0]
        
        # Create additional features
        df['Luas_kategori'] = pd.cut(df[luas_col], 
                                   bins=[0, 100, 200, 500, float('inf')], 
                                   labels=['Kecil', 'Sedang', 'Besar', 'Sangat_Besar'])
        
        # Convert Luas_kategori to string to avoid categorical issues
        df['Luas_kategori'] = df['Luas_kategori'].astype(str)
        
        # Convert categorical columns to string and handle missing values
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_columns:
            df[col] = df[col].astype(str).fillna('Unknown')
        
        print(f"📊 Final cleaned data shape: {df.shape}")
        return df
    
    def prepare_features(self, df):
        """Prepare features untuk training"""
        # Select feature columns based on available columns
        available_columns = df.columns.tolist()
        
        # Basic features that should be available
        basic_features = ['Kecamatan', 'Sertifikat', 'Kondisi Properti', 'Tipe Iklan', 'Aksesibilitas']
        
        # Check what's available and adapt
        self.feature_columns = []
        
        if 'Kecamatan' in available_columns:
            self.feature_columns.append('Kecamatan')
        if 'Sertifikat' in available_columns:
            self.feature_columns.append('Sertifikat')
        if 'Kondisi Properti' in available_columns:
            self.feature_columns.append('Kondisi_Properti')
            df['Kondisi_Properti'] = df['Kondisi Properti']  # Rename for consistency
        elif 'Kondisi' in available_columns:
            self.feature_columns.append('Kondisi')
        if 'Tipe Iklan' in available_columns:
            self.feature_columns.append('Tipe_Iklan')
            df['Tipe_Iklan'] = df['Tipe Iklan']  # Rename for consistency
        if 'Aksesibilitas' in available_columns:
            self.feature_columns.append('Aksesibilitas')
            
        # Numeric features
        if 'Luas Tanah' in available_columns:
            self.feature_columns.append('Luas_Tanah')
            df['Luas_Tanah'] = pd.to_numeric(df['Luas Tanah'], errors='coerce')
        elif 'Luas_m2' in available_columns:
            self.feature_columns.append('Luas_m2')
            
        if 'Luas Bangunan' in available_columns:
            self.feature_columns.append('Luas_Bangunan')
            df['Luas_Bangunan'] = pd.to_numeric(df['Luas Bangunan'], errors='coerce')
            
        if 'Kamar Tidur' in available_columns:
            self.feature_columns.append('Kamar_Tidur')
            df['Kamar_Tidur'] = pd.to_numeric(df['Kamar Tidur'], errors='coerce')
            
        if 'Kamar Mandi' in available_columns:
            self.feature_columns.append('Kamar_Mandi')
            df['Kamar_Mandi'] = pd.to_numeric(df['Kamar Mandi'], errors='coerce')
            
        # Add created features
        if 'Latitude' in df.columns:
            self.feature_columns.append('Latitude')
        if 'Longitude' in df.columns:
            self.feature_columns.append('Longitude')
        if 'Luas_kategori' in df.columns:
            self.feature_columns.append('Luas_kategori')
        
        print(f"📊 Selected features: {self.feature_columns}")
        
        # Prepare feature matrix
        X = df[self.feature_columns].copy()
        y = df[self.target_column].copy()
        
        # Fill missing values for numeric columns
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            X[col].fillna(X[col].median(), inplace=True)
        
        # Encode categorical variables
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns
        print(f"📊 Categorical columns to encode: {list(categorical_columns)}")
        
        for col in categorical_columns:
            print(f"📊 Processing column '{col}' with unique values: {X[col].unique()[:10]}")
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                X[col] = self.label_encoders[col].fit_transform(X[col].astype(str).fillna('Unknown'))
            else:
                X[col] = self.label_encoders[col].transform(X[col].astype(str).fillna('Unknown'))
        
        print(f"📊 Final X data types: {X.dtypes}")
        print(f"📊 Final X shape: {X.shape}")
        
        return X, y
    
    def train_models(self, df):
        """Train semua model machine learning"""
        print("🚀 Memulai training model...")
        
        # Prepare data
        X, y = self.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features for some models
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train models
        models_config = {
            'RandomForest': {
                'model': RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42,
                    n_jobs=-1
                ),
                'X_train': X_train,
                'X_test': X_test
            },
            'XGBoost': {
                'model': xgb.XGBRegressor(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=42
                ),
                'X_train': X_train,
                'X_test': X_test
            },
            'CatBoost': {
                'model': CatBoostRegressor(
                    iterations=100,
                    depth=6,
                    learning_rate=0.1,
                    random_seed=42,
                    verbose=False
                ),
                'X_train': X_train,
                'X_test': X_test
            }
        }
        
        results = {}
        
        for name, config in models_config.items():
            print(f"📊 Training {name}...")
            
            # Train model
            model = config['model']
            model.fit(config['X_train'], y_train)
            
            # Make predictions
            y_pred = model.predict(config['X_test'])
            
            # Calculate metrics
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred)
            
            # Cross validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
            
            results[name] = {
                'model': model,
                'mae': mae,
                'mse': mse,
                'rmse': rmse,
                'r2': r2,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
            
            # Save model
            self.models[name] = model
            
            print(f"✅ {name} - R² Score: {r2:.4f}, RMSE: {rmse:.2f}")
        
        return results
    
    def predict_price(self, input_data, model_name='RandomForest'):
        """Prediksi harga berdasarkan input"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} tidak tersedia")
        
        # Prepare input
        input_df = pd.DataFrame([input_data])
        
        # Add missing features that are created during preprocessing
        # Add default coordinates for Surabaya
        if 'Latitude' not in input_df.columns:
            input_df['Latitude'] = -7.2575
        if 'Longitude' not in input_df.columns:
            input_df['Longitude'] = 112.7521
            
        # Create Luas_kategori if missing
        if 'Luas_kategori' not in input_df.columns:
            luas_value = input_data.get('Luas_Tanah', input_data.get('Luas_Bangunan', 100))
            if luas_value <= 100:
                input_df['Luas_kategori'] = 'Kecil'
            elif luas_value <= 200:
                input_df['Luas_kategori'] = 'Sedang'
            elif luas_value <= 500:
                input_df['Luas_kategori'] = 'Besar'
            else:
                input_df['Luas_kategori'] = 'Sangat_Besar'
        
        # Handle column name mapping
        if 'Kondisi_Properti' not in input_df.columns and 'Kondisi_Properti' in input_data:
            input_df['Kondisi_Properti'] = input_data['Kondisi_Properti']
        elif 'Kondisi' in input_data:
            input_df['Kondisi_Properti'] = input_data['Kondisi']
            
        if 'Tipe_Iklan' not in input_df.columns and 'Tipe_Iklan' in input_data:
            input_df['Tipe_Iklan'] = input_data['Tipe_Iklan']
        
        # Ensure numeric columns are properly formatted
        numeric_columns = ['Luas_Tanah', 'Luas_Bangunan', 'Kamar_Tidur', 'Kamar_Mandi', 'Latitude', 'Longitude']
        for col in numeric_columns:
            if col in input_df.columns:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)
        
        # Encode categorical variables - use the exact column names that were trained
        categorical_mapping = {
            'Kecamatan': 'Kecamatan',
            'Sertifikat': 'Sertifikat', 
            'Kondisi_Properti': 'Kondisi_Properti',
            'Tipe_Iklan': 'Tipe_Iklan',
            'Aksesibilitas': 'Aksesibilitas',
            'Luas_kategori': 'Luas_kategori'
        }
        
        for original_col, encoded_col in categorical_mapping.items():
            if original_col in input_df.columns and encoded_col in self.label_encoders:
                try:
                    input_df[original_col] = self.label_encoders[encoded_col].transform([str(input_df[original_col].iloc[0])])
                except (ValueError, KeyError):
                    # Handle unseen categories
                    input_df[original_col] = 0
        
        # Select features in the same order as training
        try:
            X_input = input_df[self.feature_columns]
        except KeyError as e:
            missing_cols = [col for col in self.feature_columns if col not in input_df.columns]
            print(f"Missing columns: {missing_cols}")
            print(f"Available columns: {list(input_df.columns)}")
            print(f"Required columns: {self.feature_columns}")
            raise ValueError(f"Missing required features: {missing_cols}")
        
        # Predict
        model = self.models[model_name]
        prediction = model.predict(X_input)
        
        return float(prediction[0])
    
    def get_feature_importance(self, model_name='RandomForest'):
        """Dapatkan feature importance"""
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            feature_importance = dict(zip(self.feature_columns, importance))
            return sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        return None
    
    def save_models(self, directory='models'):
        """Simpan semua model"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Save models
        for name, model in self.models.items():
            joblib.dump(model, f"{directory}/{name.lower()}_model.pkl")
        
        # Save preprocessors
        joblib.dump(self.label_encoders, f"{directory}/label_encoders.pkl")
        joblib.dump(self.scaler, f"{directory}/scaler.pkl")
        joblib.dump(self.feature_columns, f"{directory}/feature_columns.pkl")
    
    def load_models(self, directory='models'):
        """Load semua model"""
        try:
            # Load models
            model_files = ['randomforest_model.pkl', 'xgboost_model.pkl', 'catboost_model.pkl']
            model_names = ['RandomForest', 'XGBoost', 'CatBoost']
            
            for file, name in zip(model_files, model_names):
                file_path = f"{directory}/{file}"
                if os.path.exists(file_path):
                    self.models[name] = joblib.load(file_path)
            
            # Load preprocessors
            self.label_encoders = joblib.load(f"{directory}/label_encoders.pkl")
            self.scaler = joblib.load(f"{directory}/scaler.pkl")
            self.feature_columns = joblib.load(f"{directory}/feature_columns.pkl")
            
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False

def train_and_save_models():
    """Function untuk training dan menyimpan model"""
    print("🎯 Memulai training machine learning models...")
    
    # Initialize predictor
    predictor = PropertyPricePredictor()
    
    # Load data from building dataset (has valid NJOP data)
    data_path = '../data/raw/Dataset_Bangunan_Surabaya.csv'
    df = predictor.load_data(data_path)
    
    if df is None:
        print("❌ Gagal memuat data")
        return None, None
    
    print(f"📊 Data loaded: {len(df)} records")
    
    # Train models
    results = predictor.train_models(df)
    
    # Save models
    predictor.save_models()
    
    print("✅ Models berhasil ditraining dan disimpan!")
    
    return predictor, results

if __name__ == "__main__":
    train_and_save_models()
