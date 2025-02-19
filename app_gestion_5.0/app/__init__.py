from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler

# Inicializa las instancias
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Configura la vista para login (cuando no esté autenticado)
login_manager.login_view = 'usuario.login'

# Carga el usuario por ID
@login_manager.user_loader
def load_user(user_id):
    from app.models.usuario_model import Usuario  # Importa aquí para evitar importación circular
    return Usuario.obtener_por_id(user_id)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/gestion_sistemas'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'tu_clave_secreta'

    # Inicializa las extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Importa y registra los Blueprints dentro de la función
    from app.controllers.usuario_controller import bp as usuario_bp
    app.register_blueprint(usuario_bp, url_prefix='/usuario')

    from app.controllers.recurso_controller import bp as recurso_bp
    app.register_blueprint(recurso_bp, url_prefix='/recurso')

    return app
