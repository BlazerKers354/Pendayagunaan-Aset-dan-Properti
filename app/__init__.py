from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

mysql = MySQL()  # Global instance

def create_app():
    app = Flask(__name__)
    
    # Load environment variables
    load_dotenv()
    
    # Configure app dari environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'telkom-dashboard-secret')
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'db_kp')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
    
    # Initialize MySQL with the app
    mysql.init_app(app)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    return app
