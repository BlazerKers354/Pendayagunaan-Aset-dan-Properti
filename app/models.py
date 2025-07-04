from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql

class User:
    def __init__(self, id=None, name=None, email=None, password=None, role='pengguna'):
        self.id = id
        self.name = name
        self.email = email
        self.password = password  # hashed!
        self.role = role

    @staticmethod
    def find_by_email(email):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, password, role FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()

        if row:
            return User(id=row[0], name=row[1], email=row[2], password=row[3], role=row[4])
        return None

    @staticmethod
    def find_by_id(user_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, password, role FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        cur.close()

        if row:
            return User(id=row[0], name=row[1], email=row[2], password=row[3], role=row[4])
        return None

    def set_password(self, password_plain):
        self.password = generate_password_hash(password_plain)

    def check_password(self, password_plain):
        return check_password_hash(self.password, password_plain)

    def save(self):
        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
            """, (self.name, self.email, self.password, self.role))
            mysql.connection.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"❌ Error saving user: {e}")
            return False
