from flask import Flask, app
from flask_mysqldb import MySQL

mysql = MySQL()  # Global instance

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3307
    app.config['MYSQL_PASSWORD'] = 'Arya151203F.'
    app.config['MYSQL_DB'] = 'db_kp'

    mysql.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
