


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  # Importamos bcrypt
from config import Config
import pymysql
pymysql.install_as_MySQLdb()
from flask_login import LoginManager

# Inicializamos db, login_manager, bcrypt y migrate
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()  # Inicializamos bcrypt
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)  # Inicializamos bcrypt
    migrate.init_app(app, db)
    login_manager.init_app(app)  # Inicializamos login_manager

    # Configura la ruta de login
    login_manager.login_view = 'usuario_bp.login'  # Asegúrate de que 'usuario_bp.login' coincida con el nombre de la vista

    # Importa Usuario dentro de la función para evitar importaciones circulares
    from app.models.usuario_model import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))  # Cargar el usuario por su ID

    # Registrar los blueprints
    from app.controllers.usuario_controller import usuario_bp
    from app.controllers.recurso_controller import recurso_bp  # Importa recurso_bp aquí
    app.register_blueprint(usuario_bp)
    app.register_blueprint(recurso_bp)  # Registra el blueprint de recursos

    return app
