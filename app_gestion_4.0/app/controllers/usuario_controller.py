# app/controllers/usuario_controller.py - Controlador de usuario
from flask import Blueprint, render_template

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")

@usuario_bp.route("/login")
def login():
    return render_template("usuario/login.html")