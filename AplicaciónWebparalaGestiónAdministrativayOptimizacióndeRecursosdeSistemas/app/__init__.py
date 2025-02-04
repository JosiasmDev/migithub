from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar blueprints (rutas)
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app