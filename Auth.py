import sqlite3
import hashlib
import jwt
import datetime

SECRET_KEY = "your_secret_key_here"


class AuthManager:
    def __init__(self, db_name="tickets.db"):
        self.db_name = db_name
        self.create_user_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_user_table(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'customer'
        )
        """)

        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, email, password, role="customer"):
        conn = self.connect()
        cursor = conn.cursor()

        hashed_password = self.hash_password(password)

        try:
            cursor.execute("""
            INSERT INTO users(username, email, password, role)
            VALUES (?, ?, ?, ?)
            """, (username, email, hashed_password, role))

            conn.commit()

            return {
                "success": True,
                "message": "Registration successful."
            }

        except sqlite3.IntegrityError:
            return {
                "success": False,
                "message": "Username or email already exists."
            }

        finally:
            conn.close()

    def login(self, username, password):
        conn = self.connect()
        cursor = conn.cursor()

        hashed_password = self.hash_password(password)

        cursor.execute("""
        SELECT id, username, role
        FROM users
        WHERE username=? AND password=?
        """, (username, hashed_password))

        user = cursor.fetchone()

        conn.close()

        if user:

            payload = {
                "user_id": user[0],
                "username": user[1],
                "role": user[2],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            }

            token = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm="HS256"
            )

            return {
                "success": True,
                "token": token
            }

        return {
            "success": False,
            "message": "Invalid username or password."
        }

    def verify_token(self, token):
        try:
            data = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            return data

        except jwt.ExpiredSignatureError:
            return None

        except jwt.InvalidTokenError:
            return None
