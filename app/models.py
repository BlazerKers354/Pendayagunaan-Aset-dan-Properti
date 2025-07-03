from werkzeug.security import generate_password_hash, check_password_hash
from .database import get_db_connection
import mysql.connector

class User:
    def __init__(self, id=None, name=None, email=None, password=None, role='pengguna'):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data['role']
                )
            return None
        except mysql.connector.Error as e:
            print(f"Error finding user by email: {e}")
            return None

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data['role']
                )
            return None
        except mysql.connector.Error as e:
            print(f"Error finding user by ID: {e}")
            return None

    def save(self):
        """Save user to database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if self.id:
                # Update existing user
                cursor.execute("""
                    UPDATE users SET name = %s, email = %s, password = %s, role = %s 
                    WHERE id = %s
                """, (self.name, self.email, self.password, self.role, self.id))
            else:
                # Insert new user
                cursor.execute("""
                    INSERT INTO users (name, email, password, role) 
                    VALUES (%s, %s, %s, %s)
                """, (self.name, self.email, self.password, self.role))
                self.id = cursor.lastrowid
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error saving user: {e}")
            return False

    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches hashed password"""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }
