#!/bin/bash

echo "🔄 Convirtiendo proyecto a SQLite..."

# 1. Crear database.py para vulnerable
cat > vulnerable/database.py << 'EOF'
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
EOF

# 2. Crear database.py para secure
cat > secure/database.py << 'EOF'
import sqlite3
import os
from werkzeug.security import generate_password_hash

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
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_username ON users(username)")
    
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
    conn.close()
    print("✓ Base de datos segura configurada (SQLite)")

if __name__ == "__main__":
    setup_database()
EOF

# 3. Actualizar requirements.txt
cat > vulnerable/requirements.txt << 'EOF'
Flask==3.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
EOF

cat > secure/requirements.txt << 'EOF'
Flask==3.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
Werkzeug==3.0.0
Flask-WTF==1.2.1
EOF

# 4. Actualizar app.py files
sed -i 's/import mysql.connector/import sqlite3/g' vulnerable/app.py
sed -i 's/mysql\.connector\.Error/sqlite3.Error/g' vulnerable/app.py
sed -i 's/mysql\.connector\.IntegrityError/sqlite3.IntegrityError/g' vulnerable/app.py

sed -i 's/import mysql.connector/import sqlite3/g' secure/app.py
sed -i 's/mysql\.connector\.Error/sqlite3.Error/g' secure/app.py
sed -i 's/mysql\.connector\.IntegrityError/sqlite3.IntegrityError/g' secure/app.py

# 5. Actualizar .gitignore
cat >> .gitignore << 'EOF'

# SQLite
*.db
*.sqlite
*.sqlite3
EOF

echo "✅ Conversión completa a SQLite"
echo ""
echo "Probando..."
cd vulnerable && python3 database.py
cd ../secure && python3 database.py

