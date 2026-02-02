import re

files_to_fix = ['vulnerable/app.py', 'secure/app.py']

for filepath in files_to_fix:
    print(f"🔧 Arreglando {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Buscar patrones como user[id] y cambiarlos a user['id']
    # Pero solo si no están ya entre comillas
    patterns = [
        (r"\buser\[id\]", "user['id']"),
        (r"\buser\[username\]", "user['username']"),
        (r"\buser\[password\]", "user['password']"),
        (r"\buser\[email\]", "user['email']"),
        (r"\buser\[role\]", "user['role']"),
        (r"\buser\[created_at\]", "user['created_at']"),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✅ {filepath} corregido")

print("\n🎉 Corrección completa!")
