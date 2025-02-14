# app/__init__.py - Inicialización de la aplicación
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.controllers.usuario_controller import usuario_bp
    app.register_blueprint(usuario_bp)

    return app
