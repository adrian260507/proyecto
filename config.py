import os
from dotenv import load_dotenv 

# Cargar variables del entorno
load_dotenv() 

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "C5t~u1%8W-9Ae6nzV`<5")
    # DB - Railway proporciona DATABASE_URL
    DB_HOST = os.getenv("DB_HOST", os.getenv("MYSQLHOST", "127.0.0.1"))
    DB_USER = os.getenv("DB_USER", os.getenv("MYSQLUSER", "root"))
    DB_PASSWORD = os.getenv("DB_PASSWORD", os.getenv("MYSQLPASSWORD", "ghih jrpw ffbb rjuj"))
    DB_NAME = os.getenv("DB_NAME", os.getenv("MYSQLDATABASE", "sistemagestionbd"))
    DB_PORT = int(os.getenv("DB_PORT", os.getenv("MYSQLPORT", "3306")))
    #Nuevo
    DB_USE_UNICODE = True
    DB_CHARSET = 'utf8mb4'
    DB_COLLATION = 'utf8mb4_unicode_ci'
    # Timezone
    DB_TIMEZONE = '+00:00'

    # Mail - Configuración para MailerSend
    MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY", "mlsn.e2c66f4d1a674aa5a1edb0dc4b36bfb61e433da8a230f5f72631d81f9eac5fee")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "conexa@test-r6ke4n17nyvgon12.mlsender.net")
    MAIL_DEFAULT_SENDER_NAME = os.getenv("MAIL_DEFAULT_SENDER_NAME", "Connexa Sistema")
    # App
    BASE_URL = os.getenv("BASE_URL", "https://tu-app.railway.app")
    MAIL_TEMPLATE_FOLDER = "mails"

    # Session
    SESSION_PROTECTION = 'strong'
    
    # Production settings
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    
    # Configuración del host y puerto para Railway
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")

    FLASK_PORT = int(os.getenv("PORT", "5000"))






