from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import pymysql
import os
from config import Config
from apscheduler.schedulers.background import BackgroundScheduler
from app.controllers.recurso_controller import recurso_bp


# Inicializamos db, login_manager, bcrypt y migrate
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Crear carpetas si no existen
    if not os.path.exists(app.config['BACKUP_FOLDER']):
        os.makedirs(app.config['BACKUP_FOLDER'])
    if not os.path.exists(app.config['LOG_FOLDER']):
        os.makedirs(app.config['LOG_FOLDER'])

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configura la ruta de login
    login_manager.login_view = 'usuario_bp.login'

    # Importa Usuario dentro de la función para evitar importaciones circulares
    from app.models.usuario_model import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar los blueprints
    from app.controllers.usuario_controller import usuario_bp
    app.register_blueprint(usuario_bp)
    app.register_blueprint(recurso_bp)

    # Función para inicializar el logging y scheduler, llamada directamente al inicio
    def iniciar_app():
        with app.app_context():  # Iniciar un contexto de aplicación
            from app.controllers.recurso_controller import configurar_logging, iniciar_scheduler
            configurar_logging()
            iniciar_scheduler(app)

    # Llamamos a la función de inicio de la app
    iniciar_app()

    return app