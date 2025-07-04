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
        
        # Drop old properties table if exists
        cursor.execute("DROP TABLE IF EXISTS properties")
        
        # Create properti_tanah table
        create_properti_tanah_table = """
        CREATE TABLE IF NOT EXISTS properti_tanah (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            location VARCHAR(100) NOT NULL,
            price BIGINT NOT NULL,
            land_area DECIMAL(10,2) NOT NULL,
            certificate VARCHAR(50),
            facing VARCHAR(50),
            water_source VARCHAR(50),
            internet ENUM('Ya', 'Tidak') DEFAULT 'Tidak',
            hook ENUM('Ya', 'Tidak') DEFAULT 'Tidak',
            power INT DEFAULT 0,
            road_width VARCHAR(50),
            description TEXT,
            status ENUM('aktif', 'tidak_aktif') DEFAULT 'aktif',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            created_by INT,
            FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """
        cursor.execute(create_properti_tanah_table)
        
        # Create properti_tanah_bangunan table
        create_properti_tanah_bangunan_table = """
        CREATE TABLE IF NOT EXISTS properti_tanah_bangunan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            location VARCHAR(100) NOT NULL,
            price BIGINT NOT NULL,
            land_area DECIMAL(10,2) NOT NULL,
            building_area DECIMAL(10,2) NOT NULL,
            bedrooms INT DEFAULT 0,
            bathrooms INT DEFAULT 0,
            floors INT DEFAULT 1,
            certificate VARCHAR(50),
            condition_property VARCHAR(50),
            facing VARCHAR(50),
            water_source VARCHAR(50),
            internet ENUM('Ya', 'Tidak') DEFAULT 'Tidak',
            hook ENUM('Ya', 'Tidak') DEFAULT 'Tidak',
            power INT DEFAULT 0,
            dining_room VARCHAR(50),
            living_room VARCHAR(50),
            road_width VARCHAR(50),
            furnished VARCHAR(50),
            description TEXT,
            status ENUM('aktif', 'tidak_aktif') DEFAULT 'aktif',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            created_by INT,
            FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
        """
        cursor.execute(create_properti_tanah_bangunan_table)
        
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
