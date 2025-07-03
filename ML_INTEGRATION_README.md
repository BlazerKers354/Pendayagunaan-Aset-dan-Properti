# Property Price Prediction System - Complete ML Integration

## 🎯 Overview

This project implements a comprehensive property price prediction system for Surabaya using advanced machine learning algorithms. The system integrates both Jupyter notebook-based models and Flask application models to provide accurate and reliable price predictions.

## 🏗️ System Architecture

### 1. Data Sources
- **Land Dataset**: `data/raw/Dataset_Tanah_Surabaya.csv` (8,000 records)
- **Building Dataset**: `data/raw/Dataset_Bangunan_Surabaya.csv` (8,980 records)

### 2. Machine Learning Models
- **XGBoost**: Gradient boosting with advanced optimization
- **Random Forest**: Ensemble learning with decision trees  
- **CatBoost**: Gradient boosting optimized for categorical features

### 3. Integration Components

#### A. Jupyter Notebook (`notebooks/property_price_prediction.ipynb`)
- Comprehensive ML pipeline with EDA, preprocessing, and model training
- Advanced feature engineering and model evaluation
- Export functionality for trained models

#### B. Flask Application Models (`app/ml_models.py`)
- Production-ready ML predictor class
- Real-time prediction capabilities
- Model persistence and loading

#### C. Enhanced Prediction System (`app/prediction_functions.py`)
- Combines both notebook and Flask models
- Ensemble predictions for improved accuracy
- Confidence metrics and performance analysis

## 🚀 Features

### 1. **Dual Model Architecture**
- Notebook models for research and development
- Flask models for production deployment
- Ensemble predictions combining multiple models

### 2. **Advanced Web Interface**
- Interactive prediction forms for both land and building properties
- Real-time model status monitoring
- Comprehensive results display with confidence metrics

### 3. **Model Performance Tracking**
- Individual model predictions comparison
- Ensemble prediction with confidence intervals
- Feature importance analysis

### 4. **Admin Dashboard Integration**
- Secure admin access for advanced predictions
- Model training and retraining capabilities
- Performance monitoring and analytics

## 📊 Model Performance

### Current Results (Building Dataset)
- **Random Forest**: R² = 1.0000, RMSE = 60.08
- **XGBoost**: R² = 1.0000, RMSE = 50.33  
- **CatBoost**: R² = 0.9972, RMSE = 1677.43

### Key Features Used
1. Kecamatan (District)
2. Luas Tanah (Land Area)
3. Luas Bangunan (Building Area)
4. Sertifikat (Certificate Type)
5. Kondisi Properti (Property Condition)
6. Kamar Tidur/Mandi (Bedrooms/Bathrooms)
7. Aksesibilitas (Accessibility)
8. Geographic coordinates (Latitude/Longitude)

## 🔧 Installation & Setup

### Prerequisites
```bash
pip install -r requirements.txt
```

### Required Dependencies
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- xgboost >= 1.7.0
- catboost >= 1.2.0
- flask >= 2.3.0
- mysql-connector-python >= 8.2.0

### Database Setup
1. Configure MySQL database settings in `config.py`
2. Run database initialization: `python run.py`

### Model Training
1. **Jupyter Notebook Method**:
   ```bash
   jupyter notebook notebooks/property_price_prediction.ipynb
   ```
   Run all cells to train and export models

2. **Flask Method**:
   ```bash
   cd app
   python ml_models.py
   ```

## 🌐 Usage

### 1. Starting the Application
```bash
python run.py
```
Access at: `http://127.0.0.1:5000`

### 2. Admin Prediction Interface
- Navigate to `/admin/prediction`
- Login with admin credentials
- Use the interactive form for predictions

### 3. API Endpoints

#### Enhanced Prediction API
```bash
POST /api/enhanced-predict
Content-Type: application/json

{
  "property_type": "building",
  "luas_tanah": 300,
  "luas_bangunan": 150,
  "kecamatan": "Surabaya",
  "kamar_tidur": 3,
  "kamar_mandi": 2,
  "sertifikat": "SHM",
  "kondisi_properti": "Baik"
}
```

#### Model Status API
```bash
GET /api/model-status
```

#### Model Training API
```bash
POST /api/train-models
```

## 📁 Project Structure

```
├── notebooks/
│   ├── property_price_prediction.ipynb    # Complete ML pipeline
│   └── README.md                          # Notebook documentation
├── app/
│   ├── ml_models.py                       # Flask ML models
│   ├── prediction_functions.py            # Enhanced prediction system
│   ├── routes.py                          # Flask routes with ML endpoints
│   └── templates/
│       ├── enhanced_prediction.html       # Advanced prediction interface
│       └── prediction_ml.html             # Standard prediction interface
├── models/                                # Trained model storage
│   ├── *.pkl                             # Flask model files
│   └── *.joblib                          # Notebook model files
├── data/
│   └── raw/
│       ├── Dataset_Tanah_Surabaya.csv    # Land dataset
│       └── Dataset_Bangunan_Surabaya.csv # Building dataset
└── static/                               # Web assets
```

## 🎨 Web Interface Features

### Enhanced Prediction Page
- Property type selection (Land/Building)
- Dynamic form fields based on property type
- Real-time model status indicator
- Interactive prediction results
- Ensemble prediction with confidence metrics
- Individual model comparison
- Price analysis and recommendations

### Visual Elements
- Modern responsive design
- Loading indicators
- Error handling
- Mobile-friendly interface
- Interactive charts and visualizations

## 🔍 Model Interpretation

### Feature Importance
The system automatically analyzes and displays the most important features for predictions:

1. **Geographic Features**: Kecamatan, Latitude, Longitude
2. **Physical Features**: Land area, Building area, Room counts
3. **Legal Features**: Certificate type, Property condition
4. **Market Features**: Accessibility, Advertisement type

### Confidence Metrics
- **High Confidence**: CV < 10% (models agree closely)
- **Medium Confidence**: CV 10-30% (moderate agreement)
- **Low Confidence**: CV > 30% (significant disagreement)

## 🚀 Future Enhancements

### Planned Features
1. **Real-time Market Data Integration**
2. **Historical Price Trend Analysis**  
3. **Comparative Market Analysis (CMA)**
4. **Automated Model Retraining**
5. **Advanced Visualization Dashboard**
6. **Mobile Application**

### Model Improvements
1. **Deep Learning Models** (Neural Networks)
2. **Time Series Forecasting**
3. **External Data Integration** (Economic indicators)
4. **Hyperparameter Optimization**

## 📞 Support & Maintenance

### Monitoring
- Model performance tracking
- Prediction accuracy monitoring
- System health checks
- Error logging and alerting

### Updates
- Regular model retraining with new data
- Performance optimization
- Feature engineering improvements
- Security updates

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

This project is developed for Telkom Indonesia property asset management.

---

**Last Updated**: July 3, 2025  
**Version**: 2.0  
**Status**: Production Ready ✅
