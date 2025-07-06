from flask import Flask
from flask_mysqldb import MySQL
from config import Config

# Buat objek MySQL sekali di level global
mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['MYSQL_HOST'] = Config.MYSQL_HOST
    app.config['MYSQL_USER'] = Config.MYSQL_USER
    app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
    app.config['MYSQL_PORT'] = int(Config.MYSQL_PORT)
    app.config['MYSQL_DB'] = Config.MYSQL_DB

    # Init MySQL ke app
    mysql.init_app(app)

    # Register blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
