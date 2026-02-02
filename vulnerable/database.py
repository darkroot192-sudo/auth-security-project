import sqlite3
import os

def get_db_path():
    return os.path.join(os.path.dirname(__file__), 'users.db')

def create_connection():
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

def setup_database():
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    try:
        cursor.execute("""
            INSERT INTO users (username, password, email, role) 
            VALUES (?, ?, ?, ?)
        """, ('admin', 'admin123', 'admin@test.com', 'admin'))
        
        cursor.execute("""
            INSERT INTO users (username, password, email) 
            VALUES (?, ?, ?)
        """, ('usuario', 'password123', 'user@test.com'))
    except sqlite3.IntegrityError:
        pass
    
    conn.commit()
    conn.close()
    print("✓ Base de datos vulnerable configurada (SQLite)")

if __name__ == "__main__":
    setup_database()
