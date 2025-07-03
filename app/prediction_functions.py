"""
Enhanced Prediction Functions for Property Price Prediction
Integrates both notebook-based models and existing Flask models
"""

import joblib
import pandas as pd
import numpy as np
import os
from .ml_models import PropertyPricePredictor

class EnhancedPropertyPredictor:
    def __init__(self):
        self.notebook_models = {}
        self.flask_predictor = PropertyPricePredictor()
        self.feature_names = {}
        self.scalers = {}
        
    def load_notebook_models(self, models_dir='../models'):
        """Load models trained from Jupyter notebook"""
        try:
            # Load land models
            land_models = ['land_random_forest_model.joblib', 'land_xgboost_model.joblib', 'land_catboost_model.joblib']
            building_models = ['building_random_forest_model.joblib', 'building_xgboost_model.joblib', 'building_catboost_model.joblib']
            
            for model_file in land_models:
                model_path = os.path.join(models_dir, model_file)
                if os.path.exists(model_path):
                    model_name = model_file.replace('.joblib', '').replace('_model', '')
                    self.notebook_models[model_name] = joblib.load(model_path)
                    
            for model_file in building_models:
                model_path = os.path.join(models_dir, model_file)
                if os.path.exists(model_path):
                    model_name = model_file.replace('.joblib', '').replace('_model', '')
                    self.notebook_models[model_name] = joblib.load(model_path)
            
            # Load feature names
            land_features_path = os.path.join(models_dir, 'land_feature_names.joblib')
            building_features_path = os.path.join(models_dir, 'building_feature_names.joblib')
            
            if os.path.exists(land_features_path):
                self.feature_names['land'] = joblib.load(land_features_path)
            if os.path.exists(building_features_path):
                self.feature_names['building'] = joblib.load(building_features_path)
                
            print(f"✅ Loaded {len(self.notebook_models)} notebook models")
            return True
            
        except Exception as e:
            print(f"⚠️ Error loading notebook models: {e}")
            return False
    
    def load_flask_models(self, models_dir='models'):
        """Load existing Flask models"""
        try:
            return self.flask_predictor.load_models(models_dir)
        except Exception as e:
            print(f"⚠️ Error loading Flask models: {e}")
            return False
    
    def predict_land_price(self, luas_tanah, kecamatan=None, sertifikat=None, kondisi=None, **kwargs):
        """
        Predict land price using multiple approaches
        """
        predictions = {}
        
        # Try Flask predictor first
        try:
            input_data = {
                'Luas_Tanah': luas_tanah,
                'Kecamatan': kecamatan or 'Surabaya',
                'Sertifikat': sertifikat or 'SHM',
                'Kondisi': kondisi or 'Baik',
                'Tipe_Iklan': 'Dijual',
                'Aksesibilitas': 'Baik',
                **kwargs
            }
            
            if self.flask_predictor.models:
                for model_name in ['RandomForest', 'XGBoost', 'CatBoost']:
                    if model_name in self.flask_predictor.models:
                        pred = self.flask_predictor.predict_price(input_data, model_name)
                        predictions[f'Flask_{model_name}'] = pred
        except Exception as e:
            print(f"Flask prediction error: {e}")
        
        # Try notebook models if available
        if 'land' in self.feature_names and 'land_random_forest' in self.notebook_models:
            try:
                # Create input for notebook models
                input_df = pd.DataFrame([{
                    'Luas_m2': luas_tanah,
                    'Kecamatan_encoded': 0,  # Would need proper encoding
                    'Jumlah_Penduduk': kwargs.get('jumlah_penduduk', 10000),
                    'Aksesibilitas_encoded': 1
                }])
                
                # Make predictions with notebook models
                for model_name in ['land_random_forest', 'land_xgboost', 'land_catboost']:
                    if model_name in self.notebook_models:
                        # Ensure input has all required features
                        required_features = self.feature_names['land']
                        for feature in required_features:
                            if feature not in input_df.columns:
                                input_df[feature] = 0
                        
                        input_df = input_df[required_features]
                        pred = self.notebook_models[model_name].predict(input_df)[0]
                        predictions[f'Notebook_{model_name}'] = pred
                        
            except Exception as e:
                print(f"Notebook land prediction error: {e}")
        
        return predictions
    
    def predict_building_price(self, luas_bangunan, luas_tanah, kecamatan=None, 
                             kamar_tidur=3, kamar_mandi=2, **kwargs):
        """
        Predict building price using multiple approaches
        """
        predictions = {}
        
        # Try Flask predictor
        try:
            input_data = {
                'Luas_Bangunan': luas_bangunan,
                'Luas_Tanah': luas_tanah,
                'Kecamatan': kecamatan or 'Surabaya',
                'Kamar_Tidur': kamar_tidur,
                'Kamar_Mandi': kamar_mandi,
                'Sertifikat': kwargs.get('sertifikat', 'SHM'),
                'Kondisi_Properti': kwargs.get('kondisi_properti', 'Baik'),
                'Tipe_Iklan': kwargs.get('tipe_iklan', 'Dijual'),
                'Aksesibilitas': kwargs.get('aksesibilitas', 'Baik'),
                **kwargs
            }
            
            if self.flask_predictor.models:
                for model_name in ['RandomForest', 'XGBoost', 'CatBoost']:
                    if model_name in self.flask_predictor.models:
                        pred = self.flask_predictor.predict_price(input_data, model_name)
                        predictions[f'Flask_{model_name}'] = pred
        except Exception as e:
            print(f"Flask building prediction error: {e}")
        
        # Try notebook models if available
        if 'building' in self.feature_names and 'building_random_forest' in self.notebook_models:
            try:
                # Create input for notebook models
                input_df = pd.DataFrame([{
                    'Luas_Bangunan': luas_bangunan,
                    'Luas_Tanah': luas_tanah,
                    'Kamar_Tidur': kamar_tidur,
                    'Kamar_Mandi': kamar_mandi,
                    'building_to_land_ratio': luas_bangunan / (luas_tanah + 1),
                    'Kecamatan_encoded': 0,  # Would need proper encoding
                }])
                
                # Make predictions with notebook models
                for model_name in ['building_random_forest', 'building_xgboost', 'building_catboost']:
                    if model_name in self.notebook_models:
                        # Ensure input has all required features
                        required_features = self.feature_names['building']
                        for feature in required_features:
                            if feature not in input_df.columns:
                                input_df[feature] = 0
                        
                        input_df = input_df[required_features]
                        pred = self.notebook_models[model_name].predict(input_df)[0]
                        predictions[f'Notebook_{model_name}'] = pred
                        
            except Exception as e:
                print(f"Notebook building prediction error: {e}")
        
        return predictions
    
    def get_ensemble_prediction(self, predictions, method='average'):
        """
        Combine predictions from multiple models
        """
        if not predictions:
            return None
            
        valid_predictions = [pred for pred in predictions.values() if pred > 0]
        
        if not valid_predictions:
            return None
        
        if method == 'average':
            return np.mean(valid_predictions)
        elif method == 'median':
            return np.median(valid_predictions)
        elif method == 'max':
            return np.max(valid_predictions)
        elif method == 'min':
            return np.min(valid_predictions)
        else:
            return np.mean(valid_predictions)
    
    def get_prediction_confidence(self, predictions):
        """
        Calculate confidence metrics for predictions
        """
        if not predictions or len(predictions) < 2:
            return {
                'confidence': 'Low',
                'std_deviation': 0,
                'coefficient_variation': 0
            }
        
        values = [pred for pred in predictions.values() if pred > 0]
        
        if len(values) < 2:
            return {
                'confidence': 'Low', 
                'std_deviation': 0,
                'coefficient_variation': 0
            }
        
        mean_pred = np.mean(values)
        std_pred = np.std(values)
        cv = std_pred / mean_pred if mean_pred > 0 else 0
        
        # Determine confidence level
        if cv < 0.1:
            confidence = 'High'
        elif cv < 0.3:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        return {
            'confidence': confidence,
            'std_deviation': std_pred,
            'coefficient_variation': cv
        }

# Global instance for use in Flask routes
enhanced_predictor = EnhancedPropertyPredictor()

# Initialize predictors
def initialize_predictors():
    """Initialize all prediction models"""
    print("🚀 Initializing Enhanced Property Predictor...")
    
    # Load Flask models
    flask_loaded = enhanced_predictor.load_flask_models()
    print(f"Flask models loaded: {flask_loaded}")
    
    # Load notebook models
    notebook_loaded = enhanced_predictor.load_notebook_models()
    print(f"Notebook models loaded: {notebook_loaded}")
    
    return flask_loaded or notebook_loaded

# Convenience functions for direct use
def predict_property_price(property_type, **kwargs):
    """
    Main prediction function
    
    Args:
        property_type: 'land' or 'building'
        **kwargs: Property features
    
    Returns:
        Dictionary with predictions and confidence metrics
    """
    if property_type == 'land':
        predictions = enhanced_predictor.predict_land_price(**kwargs)
    elif property_type == 'building':
        predictions = enhanced_predictor.predict_building_price(**kwargs)
    else:
        raise ValueError("property_type must be 'land' or 'building'")
    
    # Calculate ensemble prediction and confidence
    ensemble_pred = enhanced_predictor.get_ensemble_prediction(predictions)
    confidence_metrics = enhanced_predictor.get_prediction_confidence(predictions)
    
    return {
        'individual_predictions': predictions,
        'ensemble_prediction': ensemble_pred,
        'confidence_metrics': confidence_metrics,
        'formatted_prediction': f"Rp {ensemble_pred:,.0f}" if ensemble_pred else "N/A"
    }

def get_model_performance_summary():
    """Get summary of available models and their status"""
    summary = {
        'flask_models': list(enhanced_predictor.flask_predictor.models.keys()) if enhanced_predictor.flask_predictor.models else [],
        'notebook_models': list(enhanced_predictor.notebook_models.keys()),
        'total_models': len(enhanced_predictor.flask_predictor.models or {}) + len(enhanced_predictor.notebook_models),
        'feature_sets': list(enhanced_predictor.feature_names.keys())
    }
    return summary
