# app/__init__.py - Inicialización de la aplicación
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    
    # Registro de blueprints
    from app.controllers.usuario_controller import usuario_bp
    app.register_blueprint(usuario_bp)
    
    return app