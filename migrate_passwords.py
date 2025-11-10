from app import create_app
from werkzeug.security import generate_password_hash
from models.db import q_all, q_exec

app = create_app()

def migrate_scrypt_to_pbkdf2():
    """Convierte todos los hash Scrypt a PBKDF2"""
    with app.app_context():
        print("=== INICIANDO MIGRACIÓN DE CONTRASEÑAS ===")
        
        # Obtener todos los usuarios con hash Scrypt
        users = q_all("""
            SELECT ID_usuario, correo, contrasena 
            FROM usuarios 
            WHERE contrasena LIKE 'scrypt:%'
        """, dictcur=True)
        
        print(f"Usuarios a migrar: {len(users)}")
        
        # Contraseña temporal única para todos (luego deberán cambiarla)
        temporary_password = "Temp123!"
        
        for user in users:
            print(f"Migrando usuario: {user['correo']}")
            
            # Generar nuevo hash PBKDF2
            new_hash = generate_password_hash(temporary_password)
            
            # Actualizar en la base de datos
            q_exec("UPDATE usuarios SET contrasena = %s WHERE ID_usuario = %s", 
                   (new_hash, user['ID_usuario']))
            
            print(f"✅ Usuario {user['correo']} migrado")
        
        print(f"\n=== MIGRACIÓN COMPLETADA ===")
        print(f"Contraseña temporal para todos los usuarios: {temporary_password}")
        print("Los usuarios deben cambiar su contraseña después del primer login")

if __name__ == "__main__":
    migrate_scrypt_to_pbkdf2()
