import sqlite3
import hashlib
from datetime import datetime

class PasswordHasher:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed):
        return hashlib.sha256(password.encode()).hexdigest() == hashed

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('autoservice.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                middle_name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                created_date TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER,
                vin TEXT UNIQUE,
                license_plate TEXT UNIQUE,
                color TEXT,
                mileage INTEGER,
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                middle_name TEXT,
                position TEXT,
                phone TEXT,
                email TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                name TEXT NOT NULL,
                price REAL,
                duration INTEGER,
                category TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                name TEXT NOT NULL,
                price REAL,
                quantity INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 5,
                supplier TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE,
                client_id INTEGER,
                car_id INTEGER,
                employee_id INTEGER,
                created_date TEXT,
                status TEXT,
                total_cost REAL,
                payment_status TEXT,
                notes TEXT,
                FOREIGN KEY (client_id) REFERENCES clients (id),
                FOREIGN KEY (car_id) REFERENCES cars (id),
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                service_id INTEGER,
                quantity INTEGER DEFAULT 1,
                price REAL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_parts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                part_id INTEGER,
                quantity INTEGER DEFAULT 1,
                price REAL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (part_id) REFERENCES parts (id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS parts_movement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_id INTEGER,
                type TEXT,
                quantity INTEGER,
                date TEXT,
                order_id INTEGER,
                notes TEXT,
                FOREIGN KEY (part_id) REFERENCES parts (id),
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        
        self.conn.commit()
        self.create_default_admin()
    
    def create_default_admin(self):
        admin = self.fetch_one("SELECT * FROM users WHERE username = 'admin'")
        if not admin:
            hashed = PasswordHasher.hash_password('admin123')
            self.execute_query('''
                INSERT INTO users (username, password, role, full_name)
                VALUES (?, ?, ?, ?)
            ''', ('admin', hashed, 'admin', 'Главный администратор'))
    
    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor
    
    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()