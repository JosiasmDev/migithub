from flask import Blueprint, render_template
from app.models.recurso_model import Recurso
from app.utils import obtener_recursos

bp = Blueprint('recurso', __name__, url_prefix='/recurso')

@bp.route('/dashboard')
def dashboard():
    recursos = obtener_recursos()
    return render_template('dashboard.html')

@bp.route('/detalle/<int:id>')
def detalle(id):
    recurso = Recurso.query.get(id)
    return render_template('detalle.html', recurso=recurso)
