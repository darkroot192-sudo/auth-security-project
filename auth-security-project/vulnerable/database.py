import mysql.connector
from mysql.connector import Error

def create_connection():
    """Crear conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='vulnerable_auth',
            user='appuser',
            password='password123',
            port=3306
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

def setup_database():
    """Crear la base de datos y tabla de usuarios"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='appuser',
            password='password123',
            port=3306
        )
        
        cursor = connection.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS vulnerable_auth")
        cursor.execute("USE vulnerable_auth")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                role VARCHAR(20) DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            INSERT IGNORE INTO users (username, password, email, role) 
            VALUES ('admin', 'admin123', 'admin@test.com', 'admin')
        """)
        
        cursor.execute("""
            INSERT IGNORE INTO users (username, password, email, role) 
            VALUES ('usuario', 'password123', 'user@test.com', 'user')
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("✓ Base de datos vulnerable configurada")
        
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_database()
