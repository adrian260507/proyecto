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
    # Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.sendgrid.net")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "apikey")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "Connexa <notificaciones@asistencia.conexa.com>")

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



