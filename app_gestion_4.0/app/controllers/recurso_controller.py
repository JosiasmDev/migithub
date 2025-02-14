

from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import psutil
import logging
import os
from datetime import datetime
from app import db
from app.models.recurso_model import Recurso
from app.utils import crear_backup, limpiar_backups, generar_pdf, generar_csv
import time

recurso_bp = Blueprint('recurso_bp', __name__)

# Configuración de los logs
logging.basicConfig(filename='app/static/logs/recurso.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def monitorizar_recursos():
    # Llamamos a cpu_percent con un intervalo para obtener un valor más preciso
    cpu = psutil.cpu_percent(interval=1)  # 1 segundo de intervalo
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    log_msg = f"CPU: {cpu}%, RAM: {memory}%, Disco: {disk}%"
    logging.info(log_msg)


# Iniciar la monitorización de recursos
scheduler = BackgroundScheduler()
scheduler.add_job(func=monitorizar_recursos, trigger="interval", seconds=5)
scheduler.start()

# Ruta para forzar un backup
@recurso_bp.route("/forzar-backup")
def forzar_backup():
    try:
        crear_backup()
        flash('Backup realizado con éxito', 'success')
    except Exception as e:
        flash(f'Error al realizar el backup: {e}', 'danger')
    return redirect(url_for('recurso_bp.ver_recursos'))

# Ruta para ver los logs de recursos
@recurso_bp.route("/logs")
def ver_logs():
    with open('app/static/logs/recurso.log', 'r') as f:
        logs = f.readlines()
    return render_template('recurso/detalle.html', logs=logs)

# Ruta para descargar PDF con recursos
@recurso_bp.route("/descargar-pdf")
def descargar_pdf():
    generar_pdf()  # Llamada a una función para generar PDF con los recursos
    return redirect(url_for('recurso_bp.ver_recursos'))

# Ruta para descargar CSV con recursos
@recurso_bp.route("/descargar-csv")
def descargar_csv():
    generar_csv()  # Llamada a una función para generar CSV con los recursos
    return redirect(url_for('recurso_bp.ver_recursos'))


@recurso_bp.route("/recursos")
def ver_recursos():
    recursos = {
        'cpu': psutil.cpu_percent(),
        'ram': psutil.virtual_memory().percent,
        'disco': psutil.disk_usage('/').percent
    }
    return render_template('recurso/lista.html', recursos=recursos)
    @recurso_bp.route("/limpiar-backups")
    def limpiar_backups_route():
        try:
            limpiar_backups()
            flash('Backups limpiados con éxito', 'success')
        except Exception as e:
            flash(f'Error al limpiar los backups: {e}', 'danger')
        return redirect(url_for('recurso_bp.ver_recursos'))

@recurso_bp.route("/recursos_json")
def obtener_recursos_json():
    recursos = {
        'cpu': psutil.cpu_percent(interval=1),
        'ram': psutil.virtual_memory().percent,
        'disco': psutil.disk_usage('/').percent
    }
    return jsonify(recursos)
