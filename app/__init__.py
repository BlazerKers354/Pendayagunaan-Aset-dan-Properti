from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()  # Global instance

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'your_db_name'

    mysql.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
