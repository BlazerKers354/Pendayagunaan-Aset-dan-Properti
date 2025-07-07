import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'telkom-dashboard-secret'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or 3307
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'Arya151203F.'  # Default empty password
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'db_kp'
