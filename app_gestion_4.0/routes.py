from flask import render_template, Blueprint
import requests

recurso_controller = Blueprint('recurso', __name__)

@recurso_controller.route('/imagen-perro')
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
