from app import mysql
from flask import current_app
from werkzeug.security import generate_password_hash

def init_mysql_db():
    """Create users table & default admin"""
    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'pengguna') NOT NULL DEFAULT 'pengguna'
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        # Create default admin if none exists
        cur.execute('SELECT COUNT(*) FROM users WHERE role = "admin"')
        if cur.fetchone()[0] == 0:
            hashed_pw = generate_password_hash('admin123')
            cur.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
            """, ('Administrator', 'admin@telkom.co.id', hashed_pw, 'admin'))

        mysql.connection.commit()
        cur.close()
        print("✅ DB check done: users table ready, admin ensured.")
    except Exception as e:
        print(f"❌ Error init DB: {e}")
