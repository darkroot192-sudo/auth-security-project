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
<img width="1366" height="736" alt="image" src="https://github.com/user-attachments/assets/ed1290d5-6bb9-483a-ae2e-defb8b5bd537" />
(https://auth-security-project.onrender.com)```

### Paso 2: Probar Payload 1 (Más Efectivo)

**Campo Usuario:**
```
admin
```

**Campo Contraseña:**
```
x' OR '1'='1
```

**Click en "Entrar"**

### Comando 1: Verificar aplicación vulnerable está corriendo
| Versión | URL | Propósito |
|---------|-----|-----------|
| 🔓 Vulnerable | [auth-vulnerable.onrender.com](https://auth-security-project.onrender.com) | Demostración de vulnerabilidades |
| 🔒 Segura | [auth-secure.onrender.com](https://auth-security-project-2.onrender.com)) | Implementación segura |

## 📸 Screenshots

![Demo](docs/screenshots/demo.gif)# auth-security-demo
