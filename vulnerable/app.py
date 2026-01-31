from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from database import create_connection

app = Flask(__name__)
app.secret_key = 'clave_super_secreta_123'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = create_connection()
        if not connection:
            flash('Error de conexión', 'danger')
            return render_template('login.html')
            
        cursor = connection.cursor(dictionary=True, buffered=True)  # buffered=True
        
        # VULNERABLE: SQL Injection
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"Query ejecutada: {query}")
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()  # Solo toma el primer resultado
            
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash('Login exitoso!', 'success')
                return redirect('/dashboard')
            else:
                flash('Usuario o contraseña incorrectos', 'danger')
                
        except mysql.connector.Error as e:
            flash(f'Error SQL: {str(e)}', 'danger')
            print(f"ERROR SQL: {e}")
        finally:
            cursor.close()
            connection.close()
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        connection = create_connection()
        cursor = connection.cursor(buffered=True)
        
        try:
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            connection.commit()
            flash('Usuario registrado exitosamente!', 'success')
            return redirect('/login')
        except mysql.connector.Error as e:
            flash(f'Error al registrar: {str(e)}', 'danger')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Debes iniciar sesión', 'warning')
        return redirect('/login')
    
    # VULNERABLE: XSS
    message = request.args.get('message', '')
    
    return render_template('dashboard.html', 
                         username=session.get('username'),
                         message=message,
                         role=session.get('role'))

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Debes iniciar sesión', 'warning')
        return redirect('/login')
    
    user_id = request.args.get('id', session['user_id'])
    
    connection = create_connection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    
    try:
        cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
        user = cursor.fetchone()
    except mysql.connector.Error as e:
        flash(f'Error: {str(e)}', 'danger')
        user = None
    finally:
        cursor.close()
        connection.close()
    
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
if __name__ == '__main__':
    import os
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)

