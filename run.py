from app import create_app
import os
from models import crear_tablas

app = create_app()

def verificar_y_crear_tablas():
    """Verifica y crea las tablas si no existen"""
    try:
        print("🔄 Verificando estructura de la base de datos...")
        crear_tablas()
        print("✅ Base de datos verificada y actualizada correctamente")
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {e}")
        raise

if __name__ == "__main__":
    # Verificar tablas antes de iniciar la aplicación
    verificar_y_crear_tablas()
    
    # Configurar el modo debug desde variables de entorno
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    
    # Ejecutar la aplicación con manejo de errores
    try:
        # Railway usa el puerto de la variable de entorno PORT
        port = int(os.getenv("PORT", 5000))
        host = os.getenv("FLASK_HOST", "0.0.0.0")
        
        print(f"🚀 Iniciando aplicación en {host}:{port}")
        app.run(
            debug=debug_mode,
            host=host,
            port=port
        )
    except Exception as e:
        app.logger.error(f"Error al iniciar la aplicación: {e}")
        raise