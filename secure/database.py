import sqlite3
import os
from werkzeug.security import generate_password_hash

def get_db_path():
    return os.path.join(os.path.dirname(__file__), 'users.db')

def create_connection():
    """Crear conexión segura a SQLite"""
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def setup_database():
    """Crear la base de datos y tabla con contraseñas hasheadas"""
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    
    print("🔒 Creando base de datos segura (SQLite)...")
    
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
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON users(username)")
    
    print("🔐 Insertando usuarios con contraseñas hasheadas (bcrypt)...")
    
    admin_password = generate_password_hash('admin123')
    user_password = generate_password_hash('password123')
    
    try:
        cursor.execute("""
            INSERT INTO users (username, password, email, role) 
            VALUES (?, ?, ?, ?)
        """, ('admin', admin_password, 'admin@test.com', 'admin'))
        
        cursor.execute("""
            INSERT INTO users (username, password, email) 
            VALUES (?, ?, ?)
        """, ('usuario', user_password, 'user@test.com'))
    except sqlite3.IntegrityError:
        pass
    
    conn.commit()
    
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    print(f"✅ Usuarios creados: {len(users)}")
    for user in users:
        print(f"   - {user['username']} ({user['role']})")
    
    conn.close()
    print("\n✅ Base de datos segura configurada correctamente")

if __name__ == "__main__":
    setup_database()
