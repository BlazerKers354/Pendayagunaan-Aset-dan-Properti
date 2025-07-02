from flask import Flask
import os
from .database import init_mysql_db

def create_app():
    app = Flask(__name__)
    
    # Configure app with MySQL settings
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'telkom-dashboard-secret')
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'db_kp')
    
    # Initialize MySQL database
    with app.app_context():
        try:
            init_mysql_db()
        except Exception as e:
            print(f"Warning: Could not initialize MySQL database: {e}")
            print("Please make sure MySQL server is running and database 'db_kp' exists")

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
