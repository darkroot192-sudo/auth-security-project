# 📊 Comparativa Técnica: Vulnerable vs Seguro

## SQL Injection

### Vulnerable
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

### Seguro
```python
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
if user and check_password_hash(user['password'], password):
    # Login exitoso
```

**Mejoras:**
- ✅ Prepared statements
- ✅ Separación de verificación de contraseña
- ✅ Hash comparison en lugar de query directa

---

## XSS (Cross-Site Scripting)

### Vulnerable
```html
{{ message|safe }}
```

### Seguro
```python
from markupsafe import escape
message = escape(request.args.get('message', ''))
```
```html
{{ message }}
```

**Mejoras:**
- ✅ Escape de HTML
- ✅ Sin filtro `|safe`
- ✅ Headers CSP

---

## IDOR

### Vulnerable
```python
user_id = request.args.get('id', session['user_id'])
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

### Seguro
```python
requested_id = int(request.args.get('id', session['user_id']))
if requested_id != session['user_id'] and session.get('role') != 'admin':
    return "No tienes permiso", 403
```

**Mejoras:**
- ✅ Validación de autorización
- ✅ Solo admin puede ver otros perfiles
- ✅ Prepared statement

---

## Password Storage

### Vulnerable
```python
password = request.form['password']
query = "INSERT INTO users VALUES (%s, %s, %s)"
cursor.execute(query, (username, password, email))
```

### Seguro
```python
from werkzeug.security import generate_password_hash
hashed_password = generate_password_hash(password)
query = "INSERT INTO users VALUES (%s, %s, %s)"
cursor.execute(query, (username, hashed_password, email))
```

**Mejoras:**
- ✅ Bcrypt hashing
- ✅ Salt automático
- ✅ Verificación con `check_password_hash()`

