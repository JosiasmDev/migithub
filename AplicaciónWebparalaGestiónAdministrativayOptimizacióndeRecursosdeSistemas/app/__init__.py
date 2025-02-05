from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar la base de datos
    db.init_app(app)

    # Inicializar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Ruta para el inicio de sesión

    # Registrar blueprints (rutas)
    from app.routes import main_routes
    from app.auth import auth_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    return app