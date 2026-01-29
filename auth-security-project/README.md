# Sistema de Autenticación - Proyecto de Ciberseguridad

## Demostración de Vulnerabilidades y Remediación

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-11.8-orange.svg)](https://mariadb.org/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)]()

---

## Descripción

Proyecto educativo que demuestra vulnerabilidades comunes en aplicaciones web (OWASP Top 10) y sus respectivas soluciones implementadas. Incluye dos versiones completas:

- **Versión Vulnerable:** Contiene 4 vulnerabilidades críticas intencionadas
- **Versión Segura:** Implementa todas las correcciones y mejores prácticas

---

## Vulnerabilidades Demostradas

| # | Vulnerabilidad | Severidad | CWE | CVSS |
|---|----------------|-----------|-----|------|
| 1 | SQL Injection | CRÍTICA | CWE-89 | 9.8 |
| 2 | Cross-Site Scripting (XSS) | ALTA | CWE-79 | 7.5 |
| 3 | Insecure Direct Object Reference (IDOR) | ALTA | CWE-639 | 7.1 |
| 4 | Contraseñas en Texto Plano | CRÍTICA | CWE-256 | 9.1 |

---

## Tecnologías Utilizadas

- **Backend:** Python 3.13, Flask 3.0.0
- **Base de Datos:** MariaDB 11.8
- **Frontend:** HTML5, CSS3, JavaScript
- **Seguridad:** Werkzeug (password hashing), Flask-WTF (CSRF)

---

## Estructura del Proyecto
```
auth-security-project/
├── vulnerable/           # Versión vulnerable
│   ├── app.py
│   ├── database.py
│   ├── templates/
│   └── static/
├── secure/              # Versión segura
│   ├── app.py
│   ├── database.py
│   ├── .env
│   ├── templates/
│   └── static/
│       └── style.css
├── docs/                # Documentación
├── scripts/             # Scripts de pentesting
├── venv/                # Entorno virtual
└── README.md
```

---

## Instalación

### Requisitos Previos
- Python 3.10+
- MariaDB/MySQL 10.5+
- pip

### Pasos de Instalación
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/auth-security-project.git
cd auth-security-project

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install Flask==3.0.0 mysql-connector-python==8.2.0 werkzeug==3.0.0 python-dotenv==1.0.0 Flask-WTF==1.2.1

# 4. Configurar MariaDB
sudo mariadb
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON *.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 5. Crear bases de datos
cd vulnerable && python database.py
cd ../secure && python database.py

# 6. Ejecutar ambas versiones
# Terminal 1:
cd vulnerable && python app.py

# Terminal 2:
cd secure && python app.py
```

---

## Uso

### Versión Vulnerable (Puerto 5000)
```
http://localhost:5000
Usuario: admin
Contraseña: admin123
```

**Pruebas de Pentesting:**
- SQL Injection: `admin' OR '1'='1' --`
- XSS: `?message=<script>alert('XSS')</script>`
- IDOR: `?id=2`

### Versión Segura (Puerto 5001)
```
http://localhost:5001
Usuario: admin
Contraseña: admin123
```

---

## Características de Seguridad (Versión Segura)

**Prepared Statements** - Prevención de SQL Injection  
**Password Hashing** - Bcrypt con salt automático  
**HTML Escaping** - Protección contra XSS  
**Authorization Checks** - Validación de permisos (IDOR Fix)  
**CSRF Tokens** - Protección contra ataques CSRF  
**Security Headers** - CSP, X-Frame-Options, etc.  

---

## Comparativa de Código

### SQL Injection

**Vulnerable:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**Seguro:**
```python
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

### Password Storage


**Vulnerable:**
```python
cursor.execute(query, (username, password, email))
```

**Seguro:**
```python
hashed_password = generate_password_hash(password)
cursor.execute(query, (username, hashed_password, email))
```

---

## Propósito Educativo

Este proyecto fue creado con fines **exclusivamente educativos** para:

- Aprender sobre vulnerabilidades web comunes
- Practicar pentesting en ambiente controlado
- Comprender técnicas de remediación
- Desarrollar habilidades en ciberseguridad

### Advertencia Legal

**IMPORTANTE:** Este software es únicamente para propósitos educativos.

NO debe ser utilizado en:
- Sistemas de producción
- Entornos con datos reales
- Infraestructura sin autorización explícita

---

## Autor

**Anastacio Mariscal Otoniel**
- Estudiante de Ingeniería en Sistemas Computacionales
- Técnico en Informática
- Especialización: Ciberseguridad y Desarrollo Web

---

##Licencia

Este proyecto está bajo licencia MIT para propósitos educativos.

---

## Agradecimientos

- OWASP por el framework de seguridad
- Flask Team por el excelente framework
- Comunidad de Ciberseguridad

---

**Última actualización:** Diciembre 2025  
**Versión:** 1.0.0  
**Estado:** Funcional
