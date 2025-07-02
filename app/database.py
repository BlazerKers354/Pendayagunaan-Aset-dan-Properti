import mysql.connector
from mysql.connector import Error
from flask import current_app
import logging

def get_db_connection():
    """Get MySQL database connection"""
    try:
        connection = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            database=current_app.config['MYSQL_DB'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        raise e

def init_mysql_db():
    """Initialize MySQL database with required tables"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Create users table if it doesn't exist
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'pengguna') NOT NULL DEFAULT 'pengguna'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """
        cursor.execute(create_users_table)
        
        # Check if admin user exists, if not create one
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
        admin_count = cursor.fetchone()[0]
        
        if admin_count == 0:
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
            ''', ('Administrator', 'admin@telkom.co.id', hashed_password, 'admin'))
            
        connection.commit()
        cursor.close()
        connection.close()
        
        print("MySQL database initialized successfully")
        
    except Error as e:
        logging.error(f"Error initializing MySQL database: {e}")
        raise e

def execute_query(query, params=None, fetch=False):
    """Execute a query on the MySQL database"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if fetch:
            if fetch == 'one':
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
        else:
            result = None
            
        connection.commit()
        cursor.close()
        connection.close()
        
        return result
        
    except Error as e:
        logging.error(f"Error executing query: {e}")
        raise e
