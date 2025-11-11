from flask import Flask, render_template
from flask_mail import Mail
from flask_login import LoginManager
from config import Config
from utils.filters import register_filters
from controllers import publico_bp, auth_bp, eventos_bp, admin_bp
from models.rol import ensure_roles
from models.user import ensure_default_admin, User
from dotenv import load_dotenv

# Cargar variables del entorno (.env)
load_dotenv()

# Inicializar extensiones globales
mail = Mail()
login_manager = LoginManager()

# 📨 Importamos el cliente de MailerSend
from utils.mailersend_client import mailersend_client


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    mail.init_app(app)
    login_manager.init_app(app)
    mailersend_client.init_app(app)  # 👈 Inicializamos MailerSend aquí

    # Configuración de Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'

    # Registrar filtros Jinja personalizados
    register_filters(app)

    # Registrar blueprints
    app.register_blueprint(publico_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(eventos_bp, url_prefix="/eventos")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Manejadores de errores personalizados
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    # Bootstrap de datos esenciales
    with app.app_context():
        try:
            ensure_roles()
            ensure_default_admin()
        except Exception as e:
            app.logger.warning(f"Bootstrap warning: {e}")

    return app


@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.get_by_id(int(user_id))
