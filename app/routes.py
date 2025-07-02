from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .data_processor import AssetDataProcessor
from .models import User
import mysql.connector

main = Blueprint('main', __name__)

# Initialize data processor
data_processor = AssetDataProcessor()

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
    
    # Get detailed statistics for admin dashboard
    try:
        stats = data_processor.get_statistics()
        location_prices = data_processor.get_price_by_location()
        admin_stats = {
            'total_properties': stats.get('total_properties', 0),
            'avg_price': stats.get('avg_price', 0),
            'min_price': stats.get('min_price', 0),
            'max_price': stats.get('max_price', 0),
            'avg_land_area': stats.get('avg_land_area', 0),
            'avg_building_area': stats.get('avg_building_area', 0),
            'total_locations': len(stats.get('locations', [])),
            'locations': stats.get('locations', []),
            'conditions': stats.get('conditions', []),
            'certificates': stats.get('certificates', []),
            'location_prices': location_prices
        }
    except Exception as e:
        print(f"Error getting admin statistics: {e}")
        admin_stats = {
            'total_properties': 0,
            'avg_price': 0,
            'min_price': 0,
            'max_price': 0,
            'avg_land_area': 0,
            'avg_building_area': 0,
            'total_locations': 0,
            'locations': [],
            'conditions': [],
            'certificates': [],
            'location_prices': {}
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
    
    # Get basic statistics for dashboard
    try:
        stats = data_processor.get_statistics()
        dashboard_stats = {
            'total_properties': stats.get('total_properties', 0),
            'avg_price': stats.get('avg_price', 0),
            'total_locations': len(stats.get('locations', [])),
            'total_conditions': len(stats.get('conditions', []))
        }
    except Exception as e:
        print(f"Error getting statistics: {e}")
        dashboard_stats = {
            'total_properties': 0,
            'avg_price': 0,
            'total_locations': 0,
            'total_conditions': 0
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
    """Halaman data"""
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('main.login'))
    return render_template('data.html')

@main.route('/visualization')
def visualization():
    """Halaman visualisasi"""
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('main.login'))
    return render_template('visualization.html')

@main.route('/prediction')
def prediction():
    """Halaman prediksi"""
    if 'user_id' not in session:
        flash('Silakan login terlebih dahulu.', 'error')
        return redirect(url_for('main.login'))
    
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

@main.route('/api/properties')
def api_properties():
    """API endpoint to get property data"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        location = request.args.get('location', '')
        min_price = request.args.get('min_price', '')
        max_price = request.args.get('max_price', '')
        bedrooms = request.args.get('bedrooms', '')
        condition = request.args.get('condition', '')
        transaction_type = request.args.get('transaction_type', '')

        # Build filters
        filters = {}
        if location:
            filters['location'] = location
        if min_price:
            filters['min_price'] = int(min_price)
        if max_price:
            filters['max_price'] = int(max_price)
        if bedrooms:
            filters['bedrooms'] = int(bedrooms)
        if condition:
            filters['condition'] = condition
        if transaction_type:
            filters['transaction_type'] = transaction_type

        # Get filtered properties
        all_properties = data_processor.get_filtered_properties(filters)
        
        # Calculate pagination
        total = len(all_properties)
        start = (page - 1) * per_page
        end = start + per_page
        properties = all_properties[start:end]

        return jsonify({
            'properties': properties,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/property/<int:property_id>')
def api_property_detail(property_id):
    """API endpoint to get specific property details"""
    try:
        property_data = data_processor.get_property_by_id(property_id)
        if property_data:
            return jsonify(property_data)
        else:
            return jsonify({'error': 'Property not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/statistics')
def api_statistics():
    """API endpoint to get dataset statistics"""
    try:
        stats = data_processor.get_statistics()
        location_prices = data_processor.get_price_by_location()
        stats['location_prices'] = location_prices
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/locations')
def api_locations():
    """API endpoint to get available locations"""
    try:
        stats = data_processor.get_statistics()
        return jsonify({
            'locations': stats.get('locations', [])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/transaction-types')
def api_transaction_types():
    """API endpoint to get available transaction types"""
    try:
        if data_processor.df is not None and 'Tipe Iklan' in data_processor.df.columns:
            transaction_types = [t for t in data_processor.df['Tipe Iklan'].dropna().unique() if t and t != '']
            return jsonify({
                'transaction_types': transaction_types
            })
        else:
            return jsonify({
                'transaction_types': ['Dijual', 'Disewa', 'Keduanya']
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
