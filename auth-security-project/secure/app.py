from flask import Flask, render_template, request, redirect, session, flash
from markupsafe import escape
import mysql.connector
from database import create_connection
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Protección CSRF
csrf = CSRFProtect(app)

# Headers de seguridad
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validación de entrada
        if not username or not password:
            flash('Usuario y contraseña son requeridos', 'danger')
            return render_template('login.html')
        
        if len(username) > 50:
            flash('Usuario inválido', 'danger')
            return render_template('login.html')
        
        connection = create_connection()
        if not connection:
            flash('Error de conexión a la base de datos', 'danger')
            return render_template('login.html')
        
        cursor = connection.cursor(dictionary=True)
        
        # SEGURO: Prepared statement (previene SQL Injection)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        # SEGURO: Verificación de hash de contraseña
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session.permanent = True
            flash('Login exitoso!', 'success')
            return redirect('/dashboard')
        else:
            flash('Credenciales incorrectas', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        email = request.form.get('email', '').strip()
        
        # Validaciones
        if not username or not password or not email:
            flash('Todos los campos son requeridos', 'danger')
            return render_template('register.html')
        
        if len(username) < 3 or len(username) > 50:
            flash('El usuario debe tener entre 3 y 50 caracteres', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            return render_template('register.html')
        
        connection = create_connection()
        if not connection:
            flash('Error de conexión', 'danger')
            return render_template('register.html')
        
        cursor = connection.cursor()
        
        try:
            # SEGURO: Hash de contraseña con bcrypt
            hashed_password = generate_password_hash(password)
            
            # SEGURO: Prepared statement
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, hashed_password, email))
            
            connection.commit()
            flash('Usuario registrado exitosamente!', 'success')
            return redirect('/login')
        except mysql.connector.IntegrityError:
            flash('El usuario ya existe', 'danger')
        except Exception as e:
            flash('Error al registrar usuario', 'danger')
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    # SEGURO: Verificación de sesión
    if 'user_id' not in session:
        flash('Debes iniciar sesión', 'warning')
        return redirect('/login')
    
    # SEGURO: Escape de HTML (XSS prevention)
    message = request.args.get('message', '')
    
    return render_template('dashboard.html', 
                         username=session.get('username'),
                         message=escape(message),
                         role=session.get('role'))

@app.route('/profile')
def profile():
    # SEGURO: Verificación de sesión
    if 'user_id' not in session:
        flash('Debes iniciar sesión', 'warning')
        return redirect('/login')
    
    # SEGURO: Validación de autorización (previene IDOR)
    requested_id = request.args.get('id', session['user_id'])
    
    try:
        requested_id = int(requested_id)
    except ValueError:
        flash('ID inválido', 'danger')
        return redirect('/dashboard')
    
    # Solo permitir ver el propio perfil (o admin puede ver todos)
    if requested_id != session['user_id'] and session.get('role') != 'admin':
        flash('No tienes permiso para ver este perfil', 'danger')
        return redirect('/dashboard')
    
    connection = create_connection()
    if not connection:
        flash('Error de conexión', 'danger')
        return redirect('/dashboard')
    
    cursor = connection.cursor(dictionary=True)
    
    # SEGURO: Prepared statement + No se devuelve la contraseña
    query = "SELECT id, username, email, role, created_at FROM users WHERE id = %s"
    cursor.execute(query, (requested_id,))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()
    
    if not user:
        flash('Usuario no encontrado', 'danger')
        return redirect('/dashboard')
    
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
