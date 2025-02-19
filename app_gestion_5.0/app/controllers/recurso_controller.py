from flask import Blueprint, render_template
from app.models.recurso_model import Recurso
from app.utils import obtener_recursos
import requests

bp = Blueprint('recurso', __name__, url_prefix='/recurso')

@bp.route('/dashboard')
def dashboard():
    recursos = obtener_recursos()
    return render_template('dashboard.html')

@bp.route('/detalle/<int:id>')
def detalle(id):
    recurso = Recurso.query.get(id)
    return render_template('detalle.html', recurso=recurso)

@bp.route('/imagen-perro')
def imagen_perro():
    try:
        respuesta = requests.get("https://dog.ceo/api/breeds/image/random")
        if respuesta.status_code == 200:
            imagen_url = respuesta.json().get("message", "")
        else:
            imagen_url = None
    except Exception as e:
        print(f"Error al obtener la imagen: {e}")
        imagen_url = None

    return render_template('recurso/imagen_perro.html', imagen_url=imagen_url)
