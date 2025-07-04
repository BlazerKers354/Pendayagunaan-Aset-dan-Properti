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

class PropertiTanah:
    def __init__(self, id=None, title=None, location=None, price=None, land_area=None,
                 certificate=None, facing=None, water_source=None, internet='Tidak',
                 hook='Tidak', power=0, road_width=None, description=None, 
                 status='aktif', created_by=None):
        self.id = id
        self.title = title
        self.location = location
        self.price = price
        self.land_area = land_area
        self.certificate = certificate
        self.facing = facing
        self.water_source = water_source
        self.internet = internet
        self.hook = hook
        self.power = power
        self.road_width = road_width
        self.description = description
        self.status = status
        self.created_by = created_by

    @staticmethod
    def get_all(limit=None, offset=0, filters=None):
        """Get all properti tanah with optional filters"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM properti_tanah WHERE 1=1"
            params = []
            
            if filters:
                if filters.get('status'):
                    query += " AND status = %s"
                    params.append(filters['status'])
                if filters.get('location'):
                    query += " AND location LIKE %s"
                    params.append(f"%{filters['location']}%")
                if filters.get('price_min'):
                    query += " AND price >= %s"
                    params.append(filters['price_min'])
                if filters.get('price_max'):
                    query += " AND price <= %s"
                    params.append(filters['price_max'])
            
            query += " ORDER BY created_at DESC"
            
            if limit:
                query += " LIMIT %s OFFSET %s"
                params.extend([limit, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return [PropertiTanah(**row) for row in results]
        except mysql.connector.Error as e:
            print(f"Error getting properti tanah: {e}")
            return []

    @staticmethod
    def get_by_id(property_id):
        """Get properti tanah by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM properti_tanah WHERE id = %s", (property_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                return PropertiTanah(**result)
            return None
        except mysql.connector.Error as e:
            print(f"Error getting properti tanah by ID: {e}")
            return None

    def save(self):
        """Save properti tanah to database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if self.id:
                # Update existing property
                cursor.execute("""
                    UPDATE properti_tanah SET 
                    title = %s, location = %s, price = %s, land_area = %s,
                    certificate = %s, facing = %s, water_source = %s, 
                    internet = %s, hook = %s, power = %s, road_width = %s,
                    description = %s, status = %s
                    WHERE id = %s
                """, (self.title, self.location, self.price, self.land_area,
                      self.certificate, self.facing, self.water_source,
                      self.internet, self.hook, self.power, self.road_width,
                      self.description, self.status, self.id))
            else:
                # Insert new property
                cursor.execute("""
                    INSERT INTO properti_tanah 
                    (title, location, price, land_area, certificate, facing, 
                     water_source, internet, hook, power, road_width, 
                     description, status, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (self.title, self.location, self.price, self.land_area,
                      self.certificate, self.facing, self.water_source,
                      self.internet, self.hook, self.power, self.road_width,
                      self.description, self.status, self.created_by))
                self.id = cursor.lastrowid
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error saving properti tanah: {e}")
            return False

    def delete(self):
        """Delete properti tanah from database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM properti_tanah WHERE id = %s", (self.id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error deleting properti tanah: {e}")
            return False

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'price': self.price,
            'land_area': float(self.land_area) if self.land_area else 0,
            'certificate': self.certificate,
            'facing': self.facing,
            'water_source': self.water_source,
            'internet': self.internet,
            'hook': self.hook,
            'power': self.power,
            'road_width': self.road_width,
            'description': self.description,
            'status': self.status,
            'property_type': 'tanah',
            'created_by': self.created_by
        }

class PropertiTanahBangunan:
    def __init__(self, id=None, title=None, location=None, price=None, land_area=None,
                 building_area=None, bedrooms=0, bathrooms=0, floors=1,
                 certificate=None, condition_property=None, facing=None, 
                 water_source=None, internet='Tidak', hook='Tidak', power=0,
                 dining_room=None, living_room=None, road_width=None, furnished=None,
                 description=None, status='aktif', created_by=None):
        self.id = id
        self.title = title
        self.location = location
        self.price = price
        self.land_area = land_area
        self.building_area = building_area
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.floors = floors
        self.certificate = certificate
        self.condition_property = condition_property
        self.facing = facing
        self.water_source = water_source
        self.internet = internet
        self.hook = hook
        self.power = power
        self.dining_room = dining_room
        self.living_room = living_room
        self.road_width = road_width
        self.furnished = furnished
        self.description = description
        self.status = status
        self.created_by = created_by

    @staticmethod
    def get_all(limit=None, offset=0, filters=None):
        """Get all properti tanah+bangunan with optional filters"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM properti_tanah_bangunan WHERE 1=1"
            params = []
            
            if filters:
                if filters.get('status'):
                    query += " AND status = %s"
                    params.append(filters['status'])
                if filters.get('location'):
                    query += " AND location LIKE %s"
                    params.append(f"%{filters['location']}%")
                if filters.get('price_min'):
                    query += " AND price >= %s"
                    params.append(filters['price_min'])
                if filters.get('price_max'):
                    query += " AND price <= %s"
                    params.append(filters['price_max'])
                if filters.get('bedrooms'):
                    query += " AND bedrooms >= %s"
                    params.append(filters['bedrooms'])
            
            query += " ORDER BY created_at DESC"
            
            if limit:
                query += " LIMIT %s OFFSET %s"
                params.extend([limit, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return [PropertiTanahBangunan(**row) for row in results]
        except mysql.connector.Error as e:
            print(f"Error getting properti tanah bangunan: {e}")
            return []

    @staticmethod
    def get_by_id(property_id):
        """Get properti tanah+bangunan by ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM properti_tanah_bangunan WHERE id = %s", (property_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                return PropertiTanahBangunan(**result)
            return None
        except mysql.connector.Error as e:
            print(f"Error getting properti tanah bangunan by ID: {e}")
            return None

    def save(self):
        """Save properti tanah+bangunan to database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if self.id:
                # Update existing property
                cursor.execute("""
                    UPDATE properti_tanah_bangunan SET 
                    title = %s, location = %s, price = %s, land_area = %s,
                    building_area = %s, bedrooms = %s, bathrooms = %s, floors = %s,
                    certificate = %s, condition_property = %s, facing = %s, 
                    water_source = %s, internet = %s, hook = %s, power = %s,
                    dining_room = %s, living_room = %s, road_width = %s, 
                    furnished = %s, description = %s, status = %s
                    WHERE id = %s
                """, (self.title, self.location, self.price, self.land_area,
                      self.building_area, self.bedrooms, self.bathrooms, self.floors,
                      self.certificate, self.condition_property, self.facing,
                      self.water_source, self.internet, self.hook, self.power,
                      self.dining_room, self.living_room, self.road_width,
                      self.furnished, self.description, self.status, self.id))
            else:
                # Insert new property
                cursor.execute("""
                    INSERT INTO properti_tanah_bangunan 
                    (title, location, price, land_area, building_area, bedrooms, 
                     bathrooms, floors, certificate, condition_property, facing, 
                     water_source, internet, hook, power, dining_room, living_room,
                     road_width, furnished, description, status, created_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (self.title, self.location, self.price, self.land_area,
                      self.building_area, self.bedrooms, self.bathrooms, self.floors,
                      self.certificate, self.condition_property, self.facing,
                      self.water_source, self.internet, self.hook, self.power,
                      self.dining_room, self.living_room, self.road_width,
                      self.furnished, self.description, self.status, self.created_by))
                self.id = cursor.lastrowid
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error saving properti tanah bangunan: {e}")
            return False

    def delete(self):
        """Delete properti tanah+bangunan from database"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM properti_tanah_bangunan WHERE id = %s", (self.id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except mysql.connector.Error as e:
            print(f"Error deleting properti tanah bangunan: {e}")
            return False

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'price': self.price,
            'land_area': float(self.land_area) if self.land_area else 0,
            'building_area': float(self.building_area) if self.building_area else 0,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'floors': self.floors,
            'certificate': self.certificate,
            'condition_property': self.condition_property,
            'facing': self.facing,
            'water_source': self.water_source,
            'internet': self.internet,
            'hook': self.hook,
            'power': self.power,
            'dining_room': self.dining_room,
            'living_room': self.living_room,
            'road_width': self.road_width,
            'furnished': self.furnished,
            'description': self.description,
            'status': self.status,
            'property_type': 'tanah_bangunan',
            'created_by': self.created_by
        }
