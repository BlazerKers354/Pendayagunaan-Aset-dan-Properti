# Property Price Prediction Notebook

## Overview
This Jupyter notebook implements a comprehensive machine learning pipeline for predicting property prices in Surabaya using three advanced algorithms: XGBoost, Random Forest, and CatBoost.

## Dataset Information
- **Land Dataset**: 8,000 records with 9 features including location, area, certificate type, condition, and NJOP (tax object sale value)
- **Building Dataset**: 8,980 records with 22 features including bedrooms, bathrooms, land area, building area, utilities, and NJOP

## Notebook Structure

### 1. Setup and Data Loading
- Library imports (pandas, scikit-learn, xgboost, catboost, etc.)
- Dataset loading and initial exploration
- Data quality assessment

### 2. Exploratory Data Analysis (EDA)
- Statistical summaries
- Distribution analysis
- Correlation analysis
- Target variable exploration

### 3. Data Preprocessing
- Missing value handling
- Outlier treatment
- Feature engineering
- Categorical encoding
- Data scaling

### 4. Model Training
- **Random Forest**: Ensemble method with decision trees
- **XGBoost**: Gradient boosting with advanced optimization
- **CatBoost**: Gradient boosting optimized for categorical features

### 5. Model Evaluation
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- R² Score
- Feature importance analysis
- Prediction vs. actual value plots

### 6. Model Export
- Trained models saved to `../models/` directory
- Prediction functions exported for dashboard integration
- Performance comparison results

## Usage Instructions

### Before Running
1. Ensure all required packages are installed (see requirements.txt)
2. Verify dataset paths are correct
3. Update target column variables if needed

### Running the Notebook
1. Execute cells sequentially from top to bottom
2. Review data structure and identify target variables
3. Modify preprocessing parameters as needed
4. Train models and evaluate performance
5. Export models for dashboard integration

### Target Variables
- **Primary Target**: `NJOP_Rp_per_m2` (Tax Object Sale Value per square meter)
- **Alternative**: Any price-related column identified during data exploration

## Model Integration

### Dashboard Integration
The notebook exports prediction functions to `../app/prediction_functions.py` which can be imported into your Flask application:

```python
from app.prediction_functions import predict_land_price, predict_building_price

# Predict land price
land_prediction = predict_land_price(luas_tanah=500, lokasi_encoded=1)

# Predict building price  
building_prediction = predict_building_price(
    luas_bangunan=200, 
    luas_tanah=300, 
    lokasi_encoded=1
)
```

### Saved Model Files
- `land_random_forest_model.joblib`
- `land_xgboost_model.joblib`
- `land_catboost_model.joblib`
- `building_random_forest_model.joblib`
- `building_xgboost_model.joblib`
- `building_catboost_model.joblib`
- `land_feature_names.joblib`
- `building_feature_names.joblib`

## Expected Results
- Model comparison showing MAE, RMSE, and R² scores
- Feature importance rankings
- Prediction accuracy visualizations
- Ready-to-use prediction functions for web dashboard

## Next Steps
1. Review model performance and select best algorithms
2. Integrate prediction functions into Flask dashboard
3. Implement real-time price prediction features
4. Add model retraining capabilities for new data

## Dependencies
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- xgboost >= 1.7.0
- catboost >= 1.2.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- joblib >= 1.3.0

## Notes
- Ensure adequate memory for large dataset processing
- Model training may take several minutes depending on system specifications
- Results may vary slightly due to random state variations
