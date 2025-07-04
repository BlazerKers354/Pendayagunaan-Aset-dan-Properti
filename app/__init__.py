from flask import Flask
from flask_mysqldb import MySQL
import os

# Buat objek MySQL sekali di level global
mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # Konfigurasi rahasia & database
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'telkom-dashboard-secret')
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'Arya151203F.')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3307))
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'db_kp')

    # Init MySQL ke app
    mysql.init_app(app)

    # Register blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
