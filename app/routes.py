from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .data_processor import AssetDataProcessor
from .models import User, PropertiTanah, PropertiTanahBangunan
from .ml_models import PropertyPricePredictor
from .prediction_functions import enhanced_predictor, predict_property_price, get_model_performance_summary, initialize_predictors
import mysql.connector
import json
import os

main = Blueprint('main', __name__)

# Initialize data processor and ML predictor
data_processor = AssetDataProcessor()
ml_predictor = PropertyPricePredictor()

# Try to load pre-trained models
if os.path.exists('models'):
    try:
        ml_predictor.load_models()
        print("✅ Pre-trained models loaded successfully")
    except:
        print("⚠️ No pre-trained models found, will train on first prediction")

# Initialize enhanced predictors on startup
try:
    initialize_predictors()
except Exception as e:
    print(f"Warning: Could not initialize enhanced predictors: {e}")

@main.route('/')
def index():
    """Halaman utama - redirect ke dashboard jika sudah login, ke login jika belum"""
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect('/admin/dashboard')
        else:
            return redirect('/pengguna/dashboard')
    return redirect(url_for('main.login'))

@main.route('/home')
def home():
    """Halaman home alternatif"""
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = User.find_by_email(email)
            
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['role'] = user.role
                session['user_name'] = user.name  # Simpan nama user di session
                return redirect('/admin/dashboard' if user.role == 'admin' else '/pengguna/dashboard')
            else:
                flash('Email atau password salah.', 'error')
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')

    return render_template('login_register.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Registrasi selalu untuk role 'pengguna'
        role = 'pengguna'

        try:
            # Check if email already exists
            existing_user = User.find_by_email(email)
            
            if existing_user:
                flash('Email sudah digunakan.', 'error')
                return render_template('login_register.html')

            # Create new user
            new_user = User(name=name, email=email, role=role)
            new_user.set_password(password)
            
            if new_user.save():
                flash('Registrasi berhasil! Akun pengguna telah dibuat. Silakan login.', 'success')
                return redirect(url_for('main.login'))
            else:
                flash('Terjadi kesalahan saat membuat akun. Silakan coba lagi.', 'error')
                return render_template('login_register.html')
            
        except Exception as e:
            flash(f'Database error: {str(e)}', 'error')
            return render_template('login_register.html')

    return render_template('login_register.html')

@main.route('/admin/dashboard')
def admin_dashboard():
    """Dashboard untuk admin"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak. Silakan login sebagai admin.', 'error')
        return redirect(url_for('main.login'))
    
    # Get statistics from database
    try:
        stats = get_database_statistics()
        admin_stats = {
            'total_properties': stats.get('total_properties', 0),
            'avg_price': stats.get('avg_price', 0),
            'min_price': stats.get('min_price', 0),
            'max_price': stats.get('max_price', 0),
            'total_locations': stats.get('total_locations', 0),
            'locations': stats.get('locations', []),
            'tanah_count': stats.get('tanah_count', 0),
            'bangunan_count': stats.get('bangunan_count', 0)
        }
    except Exception as e:
        print(f"Error getting admin statistics: {e}")
        admin_stats = {
            'total_properties': 0,
            'avg_price': 0,
            'min_price': 0,
            'max_price': 0,
            'total_locations': 0,
            'locations': [],
            'tanah_count': 0,
            'bangunan_count': 0
        }
    
    return render_template('dashboard_admin.html', stats=admin_stats)

@main.route('/pengguna/dashboard')
def user_dashboard():
    """Dashboard untuk pengguna biasa"""
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('main.login'))
    
    # Ambil nama user dari database
    user = User.find_by_id(session['user_id'])
    user_name = user.name if user else 'Pengguna'
    session['user_name'] = user_name  # Simpan di session untuk digunakan di template
    
    # Get statistics from database
    try:
        stats = get_database_statistics()
        dashboard_stats = {
            'total_properties': stats.get('total_properties', 0),
            'avg_price': stats.get('avg_price', 0),
            'total_locations': stats.get('total_locations', 0),
            'tanah_count': stats.get('tanah_count', 0),
            'bangunan_count': stats.get('bangunan_count', 0)
        }
    except Exception as e:
        print(f"Error getting statistics: {e}")
        dashboard_stats = {
            'total_properties': 0,
            'avg_price': 0,
            'total_locations': 0,
            'tanah_count': 0,
            'bangunan_count': 0
        }
    
    return render_template('dashboard_user.html', stats=dashboard_stats)

@main.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('main.login'))

@main.route('/data')
def data():
    """Halaman data - redirect ke dashboard user"""
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('main.login'))
    # Redirect ke dashboard user karena fitur data sudah terintegrasi
    return redirect(url_for('main.user_dashboard'))

@main.route('/visualization')
def visualization():
    """Halaman visualisasi - hanya untuk admin"""
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('main.login'))
    
    # Check if user is admin
    if session.get('role') != 'admin':
        flash('Akses ditolak. Fitur ini hanya untuk administrator.', 'error')
        return redirect(url_for('main.user_dashboard'))
    
    return render_template('visualization.html')

@main.route('/prediction')
def prediction():
    """Halaman prediksi - hanya untuk admin"""
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('main.login'))
    
    # Check if user is admin
    if session.get('role') != 'admin':
        flash('Akses ditolak. Fitur ini hanya untuk administrator.', 'error')
        return redirect(url_for('main.user_dashboard'))
    
    # Get dataset insights for prediction reference
    try:
        stats = data_processor.get_statistics()
        prediction_data = {
            'avg_price': stats.get('avg_price', 0),
            'min_price': stats.get('min_price', 0),
            'max_price': stats.get('max_price', 0),
            'avg_land_area': stats.get('avg_land_area', 0),
            'avg_building_area': stats.get('avg_building_area', 0),
            'locations': stats.get('locations', [])[:10]  # Show top 10 locations
        }
    except Exception as e:
        print(f"Error getting prediction data: {e}")
        prediction_data = {
            'avg_price': 0,
            'min_price': 0,
            'max_price': 0,
            'avg_land_area': 0,
            'avg_building_area': 0,
            'locations': []
        }
    
    return render_template('prediction.html', prediction_data=prediction_data)

# Machine Learning Prediction Routes
@main.route('/admin/prediction')
def prediction_page():
    """Enhanced prediction page for admin with multiple model support"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak. Hanya admin yang dapat mengakses halaman ini.', 'error')
        return redirect(url_for('main.login'))
    
    # Get unique values for dropdowns
    try:
        stats = data_processor.get_statistics()
        form_data = {
            'kecamatan_list': sorted(stats.get('locations', [])),
            'sertifikat_list': ['SHM', 'HGB', 'Girik', 'Belum Bersertifikat'],
            'kondisi_list': ['Baik', 'Buruk'],
            'tipe_iklan_list': ['Dijual', 'Disewa', 'Disewa/Dijual'],
            'aksesibilitas_list': ['Baik', 'Buruk']
        }
    except Exception as e:
        print(f"Error getting form data: {e}")
        form_data = {
            'kecamatan_list': [],
            'sertifikat_list': ['SHM', 'HGB', 'Girik', 'Belum Bersertifikat'],
            'kondisi_list': ['Baik', 'Buruk'],
            'tipe_iklan_list': ['Dijual', 'Disewa', 'Disewa/Dijual'],
            'aksesibilitas_list': ['Baik', 'Buruk']
        }
    
    return render_template('enhanced_prediction.html', form_data=form_data)
    """Enhanced prediction page for admin with multiple model support"""
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Akses ditolak. Hanya admin yang dapat mengakses halaman ini.', 'error')
        return redirect(url_for('main.login'))
    
    # Get unique values for dropdowns
    try:
        stats = data_processor.get_statistics()
        form_data = {
            'kecamatan_list': sorted(stats.get('locations', [])),
            'sertifikat_list': ['SHM', 'HGB', 'Girik', 'Belum Bersertifikat'],
            'kondisi_list': ['Baik', 'Buruk'],
            'tipe_iklan_list': ['Dijual', 'Disewa', 'Disewa/Dijual'],
            'aksesibilitas_list': ['Baik', 'Buruk']
        }
    except Exception as e:
        print(f"Error getting form data: {e}")
        form_data = {
            'kecamatan_list': [],
            'sertifikat_list': ['SHM', 'HGB', 'Girik', 'Belum Bersertifikat'],
            'kondisi_list': ['Baik', 'Buruk'],
            'tipe_iklan_list': ['Dijual', 'Disewa', 'Disewa/Dijual'],
            'aksesibilitas_list': ['Baik', 'Buruk']
        }
    
    return render_template('enhanced_prediction.html', form_data=form_data)

@main.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint untuk prediksi harga properti"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields for building dataset
        required_fields = ['kecamatan', 'sertifikat', 'kondisi_properti', 'tipe_iklan', 'aksesibilitas']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} is required'}), 400
        
        # Prepare input data for building dataset
        input_data = {
            'Kecamatan': data['kecamatan'],
            'Sertifikat': data['sertifikat'],
            'Kondisi_Properti': data['kondisi_properti'],
            'Tipe_Iklan': data['tipe_iklan'],
            'Aksesibilitas': data['aksesibilitas'],
            'Luas_Tanah': float(data.get('luas_tanah', 200)),
            'Luas_Bangunan': float(data.get('luas_bangunan', 150)),
            'Kamar_Tidur': int(data.get('kamar_tidur', 3)),
            'Kamar_Mandi': int(data.get('kamar_mandi', 2)),
        }
        
        # Note: Latitude, Longitude, and Luas_kategori will be added automatically in predict_price method
        
        # Train models if not loaded
        if not ml_predictor.models:
            print("⚠️ Models not loaded, training new models...")
            df = ml_predictor.load_data('../data/raw/Dataset_Bangunan_Surabaya.csv')
            if df is not None:
                ml_predictor.train_models(df)
                ml_predictor.save_models()
            else:
                return jsonify({'error': 'Unable to load training data'}), 500
        
        # Get predictions from all models
        predictions = {}
        model_names = ['RandomForest', 'XGBoost', 'CatBoost']
        
        for model_name in model_names:
            if model_name in ml_predictor.models:
                try:
                    pred = ml_predictor.predict_price(input_data, model_name)
                    predictions[model_name] = {
                        'price': round(pred, 2),
                        'price_formatted': f"Rp {pred:,.0f}"
                    }
                except Exception as e:
                    print(f"Error predicting with {model_name}: {e}")
                    predictions[model_name] = {
                        'price': 0,
                        'price_formatted': "Error",
                        'error': str(e)
                    }
        
        # Calculate average prediction
        valid_predictions = [p['price'] for p in predictions.values() if p['price'] > 0]
        avg_prediction = sum(valid_predictions) / len(valid_predictions) if valid_predictions else 0
        
        # Get feature importance (from Random Forest)
        feature_importance = None
        if 'RandomForest' in ml_predictor.models:
            feature_importance = ml_predictor.get_feature_importance('RandomForest')
        
        result = {
            'success': True,
            'predictions': predictions,
            'average_prediction': {
                'price': round(avg_prediction, 2),
                'price_formatted': f"Rp {avg_prediction:,.0f}"
            },
            'input_data': input_data,
            'feature_importance': feature_importance[:5] if feature_importance else None  # Top 5 features
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@main.route('/api/train-models', methods=['POST'])
def api_train_models():
    """API endpoint untuk training ulang model"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        print("🚀 Starting model training...")
        
        # Load data and train models
        df = ml_predictor.load_data('../data/raw/Dataset_Bangunan_Surabaya.csv')
        if df is None:
            return jsonify({'error': 'Unable to load training data'}), 500
        
        # Train models
        results = ml_predictor.train_models(df)
        
        # Save models
        ml_predictor.save_models()
        
        # Format results
        formatted_results = {}
        for name, result in results.items():
            formatted_results[name] = {
                'r2_score': round(result['r2'], 4),
                'mae': round(result['mae'], 2),
                'rmse': round(result['rmse'], 2),
                'cv_mean': round(result['cv_mean'], 4),
                'cv_std': round(result['cv_std'], 4)
            }
        
        return jsonify({
            'success': True,
            'message': 'Models trained successfully',
            'results': formatted_results,
            'data_size': len(df)
        })
        
    except Exception as e:
        print(f"Training error: {e}")
        return jsonify({'error': str(e)}), 500

@main.route('/api/model-performance')
def api_model_performance():
    """API endpoint untuk mendapatkan performa model"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Check if models are loaded
        if not ml_predictor.models:
            return jsonify({
                'models_loaded': False,
                'message': 'No models loaded. Please train models first.'
            })
        
        # Get feature importance for visualization
        performance_data = {}
        
        for model_name in ml_predictor.models.keys():
            feature_importance = ml_predictor.get_feature_importance(model_name)
            if feature_importance:
                # Convert numpy float32 to Python float for JSON serialization
                feature_importance_clean = [
                    (str(feature), float(importance)) 
                    for feature, importance in feature_importance[:10]
                ]
                performance_data[model_name] = {
                    'feature_importance': feature_importance_clean,
                    'model_loaded': True
                }
            else:
                performance_data[model_name] = {
                    'feature_importance': [],
                    'model_loaded': True
                }
        
        return jsonify({
            'models_loaded': True,
            'performance_data': performance_data,
            'available_models': list(ml_predictor.models.keys())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Enhanced Machine Learning Prediction Routes
@main.route('/api/enhanced-predict', methods=['POST'])
def api_enhanced_predict():
    """Enhanced API endpoint for property price prediction using multiple models"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        property_type = data.get('property_type', 'building')
        
        # Validate required fields
        if property_type == 'building':
            required_fields = ['luas_bangunan', 'luas_tanah']
            prediction_kwargs = {
                'luas_bangunan': float(data.get('luas_bangunan', 150)),
                'luas_tanah': float(data.get('luas_tanah', 200)),
                'kecamatan': data.get('kecamatan', 'Surabaya'),
                'kamar_tidur': int(data.get('kamar_tidur', 3)),
                'kamar_mandi': int(data.get('kamar_mandi', 2)),
                'sertifikat': data.get('sertifikat', 'SHM'),
                'kondisi_properti': data.get('kondisi_properti', 'Baik'),
                'tipe_iklan': data.get('tipe_iklan', 'Dijual'),
                'aksesibilitas': data.get('aksesibilitas', 'Baik')
            }
        else:  # land
            required_fields = ['luas_tanah']
            prediction_kwargs = {
                'luas_tanah': float(data.get('luas_tanah', 200)),
                'kecamatan': data.get('kecamatan', 'Surabaya'),
                'sertifikat': data.get('sertifikat', 'SHM'),
                'kondisi': data.get('kondisi', 'Baik'),
                'jumlah_penduduk': int(data.get('jumlah_penduduk', 10000))
            }
        
        # Validate required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Field {field} is required'}), 400
        
        # Get enhanced predictions
        result = predict_property_price(property_type, **prediction_kwargs)
        
        # Add model performance summary
        model_summary = get_model_performance_summary()
        
        # Format response
        response = {
            'success': True,
            'property_type': property_type,
            'predictions': result['individual_predictions'],
            'ensemble_prediction': {
                'value': result['ensemble_prediction'],
                'formatted': result['formatted_prediction']
            },
            'confidence': result['confidence_metrics'],
            'input_data': prediction_kwargs,
            'model_summary': model_summary,
            'recommendation': _get_price_recommendation(result['ensemble_prediction'], property_type)
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Enhanced prediction error: {e}")
        return jsonify({'error': str(e)}), 500

def _get_price_recommendation(predicted_price, property_type):
    """Generate price recommendation based on prediction"""
    if not predicted_price:
        return "Unable to generate recommendation"
    
    if property_type == 'building':
        if predicted_price < 500000000:  # < 500M
            return "Harga properti tergolong rendah untuk wilayah Surabaya"
        elif predicted_price < 1000000000:  # 500M - 1B
            return "Harga properti dalam rentang menengah"
        elif predicted_price < 2000000000:  # 1B - 2B
            return "Harga properti tergolong tinggi"
        else:
            return "Harga properti sangat tinggi, lokasi premium"
    else:  # land
        if predicted_price < 200000000:  # < 200M
            return "Harga tanah tergolong rendah"
        elif predicted_price < 500000000:  # 200M - 500M
            return "Harga tanah dalam rentang menengah"
        else:
            return "Harga tanah tergolong tinggi"

@main.route('/api/model-status')
def api_model_status():
    """API endpoint to get current model status and performance"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        model_summary = get_model_performance_summary()
        
        # Add detailed status
        status = {
            'models_loaded': model_summary['total_models'] > 0,
            'flask_models_count': len(model_summary['flask_models']),
            'notebook_models_count': len(model_summary['notebook_models']),
            'available_models': model_summary['flask_models'] + model_summary['notebook_models'],
            'feature_sets': model_summary['feature_sets'],
            'last_training': "Available in models directory" if os.path.exists('models') else "No training data",
            'recommendation': "Multiple models available for ensemble predictions" if model_summary['total_models'] > 1 else "Single model predictions available"
        }
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/locations')
def api_locations():
    """API endpoint untuk mendapatkan daftar lokasi"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        locations = data_processor.get_unique_locations()
        return jsonify({'locations': locations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/properties')
def api_properties():
    """API endpoint untuk mendapatkan daftar properti dengan filter dan pagination"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        property_type = request.args.get('property_type', '')  # 'tanah' or 'tanah_bangunan'
        location = request.args.get('location', '')
        min_price = request.args.get('min_price', '')
        max_price = request.args.get('max_price', '')
        status = request.args.get('status', '')
        bedrooms = request.args.get('bedrooms', '')
        
        # Build filters
        filters = {}
        if location:
            filters['location'] = location
        if min_price:
            filters['price_min'] = float(min_price)
        if max_price:
            filters['price_max'] = float(max_price)
        if status:
            filters['status'] = status
        if bedrooms:
            filters['bedrooms'] = int(bedrooms)
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get data based on property type
        properties = []
        total_items = 0
        
        if property_type == 'tanah':
            # Get only land properties
            tanah_properties = PropertiTanah.get_all(limit=per_page, offset=offset, filters=filters)
            properties = [prop.to_dict() for prop in tanah_properties]
            
            # Get total count for pagination
            all_tanah = PropertiTanah.get_all(filters=filters)
            total_items = len(all_tanah)
            
        elif property_type == 'tanah_bangunan':
            # Get only building+land properties
            bangunan_properties = PropertiTanahBangunan.get_all(limit=per_page, offset=offset, filters=filters)
            properties = [prop.to_dict() for prop in bangunan_properties]
            
            # Get total count for pagination
            all_bangunan = PropertiTanahBangunan.get_all(filters=filters)
            total_items = len(all_bangunan)
            
        else:
            # Get both types
            tanah_properties = PropertiTanah.get_all(filters=filters)
            bangunan_properties = PropertiTanahBangunan.get_all(filters=filters)
            
            # Combine both types
            all_properties = []
            all_properties.extend([prop.to_dict() for prop in tanah_properties])
            all_properties.extend([prop.to_dict() for prop in bangunan_properties])
            
            # Sort by created_at (newest first)
            all_properties.sort(key=lambda x: x.get('id', 0), reverse=True)
            
            total_items = len(all_properties)
            properties = all_properties[offset:offset + per_page]
        
        # Calculate total pages
        total_pages = (total_items + per_page - 1) // per_page
        
        return jsonify({
            'properties': properties,
            'total': total_items,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/property/<int:property_id>')
def api_property_detail(property_id):
    """API endpoint untuk mendapatkan detail properti berdasarkan ID"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get all building data
        all_data = data_processor.get_building_data()
        
        # Find property by ID (simplified - in real app you'd have proper ID management)
        property_data = None
        for i, item in enumerate(all_data):
            if item.get('id', i) == property_id or i == property_id:
                property_data = item
                break
        
        if not property_data:
            return jsonify({'error': 'Property not found'}), 404
        
        # Format detailed property data
        property_detail = {
            'id': property_id,
            'title': f"Properti {property_data.get('kecamatan', 'Unknown')} - {property_data.get('luas_tanah', 0)} m²",
            'location': property_data.get('kecamatan', 'Unknown'),
            'price': float(property_data.get('harga', 0)),
            'land_area': float(property_data.get('luas_tanah', 0)),
            'building_area': float(property_data.get('luas_bangunan', 0) or 0),
            'bedrooms': int(property_data.get('kamar_tidur', 0) or 0),
            'bathrooms': int(property_data.get('kamar_mandi', 0) or 0),
            'condition': property_data.get('kondisi', 'N/A'),
            'certificate': property_data.get('sertifikat', 'N/A'),
            'furnished': property_data.get('furnished', 'N/A'),
            'floors': int(property_data.get('jumlah_lantai', 1) or 1),
            'facing': property_data.get('hadap', 'N/A'),
            'water_source': property_data.get('sumber_air', 'N/A'),
            'internet': property_data.get('internet', 'N/A'),
            'hook': property_data.get('hook', 'N/A'),
            'power': int(property_data.get('daya_listrik', 0) or 0),
            'dining_room': property_data.get('ruang_makan', 'N/A'),
            'living_room': property_data.get('ruang_tamu', 'N/A'),
            'road_width': property_data.get('lebar_jalan', 'N/A')
        }
        
        return jsonify(property_detail)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin API for CRUD operations
@main.route('/api/admin/properties')
def api_admin_properties():
    """API endpoint untuk admin mendapatkan semua properti"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Get parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        property_type = request.args.get('property_type', '')
        status = request.args.get('status', '')
        
        # Build filters
        filters = {}
        if status:
            filters['status'] = status
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Get data based on property type
        properties = []
        total_items = 0
        
        if property_type == 'tanah':
            tanah_properties = PropertiTanah.get_all(limit=per_page, offset=offset, filters=filters)
            properties = [prop.to_dict() for prop in tanah_properties]
            all_tanah = PropertiTanah.get_all(filters=filters)
            total_items = len(all_tanah)
        elif property_type == 'tanah_bangunan':
            bangunan_properties = PropertiTanahBangunan.get_all(limit=per_page, offset=offset, filters=filters)
            properties = [prop.to_dict() for prop in bangunan_properties]
            all_bangunan = PropertiTanahBangunan.get_all(filters=filters)
            total_items = len(all_bangunan)
        else:
            # Get both types
            tanah_properties = PropertiTanah.get_all(filters=filters)
            bangunan_properties = PropertiTanahBangunan.get_all(filters=filters)
            
            all_properties = []
            all_properties.extend([prop.to_dict() for prop in tanah_properties])
            all_properties.extend([prop.to_dict() for prop in bangunan_properties])
            
            all_properties.sort(key=lambda x: x.get('id', 0), reverse=True)
            total_items = len(all_properties)
            properties = all_properties[offset:offset + per_page]
        
        total_pages = (total_items + per_page - 1) // per_page
        
        return jsonify({
            'properties': properties,
            'total': total_items,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/admin/property', methods=['POST'])
def api_admin_create_property():
    """Create new property"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        property_type = data.get('property_type')
        
        if property_type == 'tanah':
            property_obj = PropertiTanah(
                title=data.get('title'),
                location=data.get('location'),
                price=data.get('price'),
                land_area=data.get('land_area'),
                certificate=data.get('certificate'),
                facing=data.get('facing'),
                water_source=data.get('water_source'),
                internet=data.get('internet', 'Tidak'),
                hook=data.get('hook', 'Tidak'),
                power=data.get('power', 0),
                road_width=data.get('road_width'),
                description=data.get('description'),
                status=data.get('status', 'aktif'),
                created_by=session['user_id']
            )
        else:  # tanah_bangunan
            property_obj = PropertiTanahBangunan(
                title=data.get('title'),
                location=data.get('location'),
                price=data.get('price'),
                land_area=data.get('land_area'),
                building_area=data.get('building_area'),
                bedrooms=data.get('bedrooms', 0),
                bathrooms=data.get('bathrooms', 0),
                floors=data.get('floors', 1),
                certificate=data.get('certificate'),
                condition_property=data.get('condition_property'),
                facing=data.get('facing'),
                water_source=data.get('water_source'),
                internet=data.get('internet', 'Tidak'),
                hook=data.get('hook', 'Tidak'),
                power=data.get('power', 0),
                dining_room=data.get('dining_room'),
                living_room=data.get('living_room'),
                road_width=data.get('road_width'),
                furnished=data.get('furnished'),
                description=data.get('description'),
                status=data.get('status', 'aktif'),
                created_by=session['user_id']
            )
        
        if property_obj.save():
            return jsonify({
                'success': True,
                'message': 'Property created successfully',
                'property': property_obj.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to create property'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/admin/property/<property_type>/<int:property_id>', methods=['PUT'])
def api_admin_update_property(property_type, property_id):
    """Update existing property"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        if property_type == 'tanah':
            property_obj = PropertiTanah.get_by_id(property_id)
        else:
            property_obj = PropertiTanahBangunan.get_by_id(property_id)
        
        if not property_obj:
            return jsonify({'error': 'Property not found'}), 404
        
        # Update fields
        property_obj.title = data.get('title', property_obj.title)
        property_obj.location = data.get('location', property_obj.location)
        property_obj.price = data.get('price', property_obj.price)
        property_obj.land_area = data.get('land_area', property_obj.land_area)
        property_obj.certificate = data.get('certificate', property_obj.certificate)
        property_obj.facing = data.get('facing', property_obj.facing)
        property_obj.water_source = data.get('water_source', property_obj.water_source)
        property_obj.internet = data.get('internet', property_obj.internet)
        property_obj.hook = data.get('hook', property_obj.hook)
        property_obj.power = data.get('power', property_obj.power)
        property_obj.road_width = data.get('road_width', property_obj.road_width)
        property_obj.description = data.get('description', property_obj.description)
        property_obj.status = data.get('status', property_obj.status)
        
        if property_type == 'tanah_bangunan':
            property_obj.building_area = data.get('building_area', property_obj.building_area)
            property_obj.bedrooms = data.get('bedrooms', property_obj.bedrooms)
            property_obj.bathrooms = data.get('bathrooms', property_obj.bathrooms)
            property_obj.floors = data.get('floors', property_obj.floors)
            property_obj.condition_property = data.get('condition_property', property_obj.condition_property)
            property_obj.dining_room = data.get('dining_room', property_obj.dining_room)
            property_obj.living_room = data.get('living_room', property_obj.living_room)
            property_obj.furnished = data.get('furnished', property_obj.furnished)
        
        if property_obj.save():
            return jsonify({
                'success': True,
                'message': 'Property updated successfully',
                'property': property_obj.to_dict()
            })
        else:
            return jsonify({'error': 'Failed to update property'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/admin/property/<property_type>/<int:property_id>', methods=['DELETE'])
def api_admin_delete_property(property_type, property_id):
    """Delete property"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if property_type == 'tanah':
            property_obj = PropertiTanah.get_by_id(property_id)
        elif property_type == 'tanah_bangunan':
            property_obj = PropertiTanahBangunan.get_by_id(property_id)
        else:
            return jsonify({'error': 'Invalid property type'}), 400
        
        if not property_obj:
            return jsonify({'error': 'Property not found'}), 404
        
        if property_obj.delete():
            return jsonify({
                'success': True,
                'message': 'Property deleted successfully'
            })
        else:
            return jsonify({'error': 'Failed to delete property'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/admin/property/<property_type>/<int:property_id>')
def api_admin_get_property(property_type, property_id):
    """Get single property by ID"""
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        if property_type == 'tanah':
            property_obj = PropertiTanah.get_by_id(property_id)
        else:
            property_obj = PropertiTanahBangunan.get_by_id(property_id)
        
        if not property_obj:
            return jsonify({'error': 'Property not found'}), 404
        
        return jsonify({
            'success': True,
            'property': property_obj.to_dict()
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_database_statistics():
    """Get statistics from database tables"""
    try:
        # Get all properties from both tables
        tanah_properties = PropertiTanah.get_all()
        bangunan_properties = PropertiTanahBangunan.get_all()
        
        all_properties = []
        all_properties.extend([prop.to_dict() for prop in tanah_properties])
        all_properties.extend([prop.to_dict() for prop in bangunan_properties])
        
        if not all_properties:
            return {
                'total_properties': 0,
                'avg_price': 0,
                'min_price': 0,
                'max_price': 0,
                'total_locations': 0,
                'locations': []
            }
        
        # Calculate statistics
        prices = [prop['price'] for prop in all_properties if prop['price']]
        locations = list(set([prop['location'] for prop in all_properties if prop['location']]))
        
        stats = {
            'total_properties': len(all_properties),
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'total_locations': len(locations),
            'locations': locations,
            'tanah_count': len(tanah_properties),
            'bangunan_count': len(bangunan_properties)
        }
        
        return stats
        
    except Exception as e:
        print(f"Error getting database statistics: {e}")
        return {
            'total_properties': 0,
            'avg_price': 0,
            'min_price': 0,
            'max_price': 0,
            'total_locations': 0,
            'locations': []
        }

