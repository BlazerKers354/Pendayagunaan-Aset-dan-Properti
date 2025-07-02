from flask import Flask
import sqlite3
import os
from contextlib import closing

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'telkom-dashboard-secret')
    app.config['DATABASE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance', 'app.db')
    
    # Create instance directory if it doesn't exist
    instance_dir = os.path.dirname(app.config['DATABASE'])
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    
    # Initialize database
    init_db(app.config['DATABASE'])

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app

def get_db_connection(database_path):
    """Get database connection"""
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(database_path):
    """Initialize database with required tables"""
    with closing(sqlite3.connect(database_path)) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'pengguna'
            )
        ''')
        
        # Check if admin user exists, if not create one
        cursor = conn.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash('admin123')
            conn.execute('''
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            ''', ('Administrator', 'admin@admin.com', hashed_password, 'admin'))
        
        conn.commit()
