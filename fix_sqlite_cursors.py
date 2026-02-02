import re

# Arreglar vulnerable/app.py
print("🔧 Arreglando vulnerable/app.py...")
with open('vulnerable/app.py', 'r') as f:
    content = f.read()

# Reemplazar cursors con parámetros
content = re.sub(
    r'cursor\s*=\s*connection\.cursor\([^)]*\)',
    'cursor = connection.cursor()',
    content
)

with open('vulnerable/app.py', 'w') as f:
    f.write(content)
print("✅ vulnerable/app.py corregido")

# Arreglar secure/app.py
print("🔧 Arreglando secure/app.py...")
with open('secure/app.py', 'r') as f:
    content = f.read()

content = re.sub(
    r'cursor\s*=\s*connection\.cursor\([^)]*\)',
    'cursor = connection.cursor()',
    content
)

with open('secure/app.py', 'w') as f:
    f.write(content)
print("✅ secure/app.py corregido")

print("\n🎉 Corrección completa. Ahora sube los cambios a GitHub:")
print("  git add .")
print("  git commit -m 'Fix: SQLite cursor compatibility'")
print("  git push origin main")
