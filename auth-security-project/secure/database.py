import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    """Crear conexión segura a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_DATABASE', 'secure_auth'),
            user=os.getenv('DB_USER', 'appuser'),
            password=os.getenv('DB_PASSWORD'),
            port=3306
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Error de conexión: {e}")
        return None

def setup_database():
    """Crear la base de datos y tabla de usuarios con contraseñas hasheadas"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'appuser'),
            password=os.getenv('DB_PASSWORD'),
            port=3306
        )
        
        if not connection.is_connected():
            print("❌ No se pudo conectar")
            return
            
        cursor = connection.cursor()
        
        print("🔒 Creando base de datos segura...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS secure_auth")
        cursor.execute("USE secure_auth")
        
        print("📋 Creando tabla users con índices...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_username (username)
            )
        """)
        
        print(" Insertando usuarios con contraseñas hasheadas (bcrypt)...")
        
        admin_password = generate_password_hash('admin123')
        user_password = generate_password_hash('password123')
        
        cursor.execute("""
            INSERT IGNORE INTO users (username, password, email, role) 
            VALUES (%s, %s, %s, %s)
        """, ('admin', admin_password, 'admin@test.com', 'admin'))
        
        cursor.execute("""
            INSERT IGNORE INTO users (username, password, email, role) 
            VALUES (%s, %s, %s, %s)
        """, ('usuario', user_password, 'user@test.com', 'user'))
        
        connection.commit()
        
        cursor.execute("SELECT username, role FROM users")
        users = cursor.fetchall()
        print(f" Usuarios creados: {len(users)}")
        for user in users:
            print(f"   - {user[0]} ({user[1]})")
        
        cursor.execute("SELECT username, LEFT(password, 60) FROM users WHERE username = 'admin'")
        admin = cursor.fetchone()
        print(f"\n Ejemplo de contraseña hasheada:")
        print(f"   Usuario: {admin[0]}")
        print(f"   Hash: {admin[1]}...")
        
        cursor.close()
        connection.close()
        print("\n Base de datos segura configurada correctamente")
        
    except Error as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    setup_database()
