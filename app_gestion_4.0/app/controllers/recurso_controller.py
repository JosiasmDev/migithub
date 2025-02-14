# recurso_controller.py
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, current_app
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

def configurar_logging():
    log_folder = current_app.config['LOG_FOLDER']
    logging.basicConfig(filename=os.path.join(log_folder, 'recursos.log'), 
                        level=logging.INFO, 
                        format='%(asctime)s - %(message)s')

# Configuración de los logs
# Se configura dentro de la función `create_app` después de crear la app
# logging.basicConfig(filename=os.path.join(current_app.config['LOG_FOLDER'], 'recursos.log'), 
#                     level=logging.INFO, 
#                     format='%(asctime)s - %(message)s')

def monitorizar_recursos():
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
    return redirect(url_for('usuario_bp.dashboard'))

# Ruta para ver los logs de recursos
@recurso_bp.route("/logs")
def ver_logs():
    log_file = os.path.join(current_app.config['LOG_FOLDER'], 'recursos.log')
    with open(log_file, 'r') as f:
        logs = f.readlines()
    return render_template('recurso/logs.html', logs=logs)

# Ruta para descargar PDF con recursos
@recurso_bp.route("/descargar-pdf")
def descargar_pdf():
    pdf_file = generar_pdf()
    return send_file(pdf_file, as_attachment=True)

# Ruta para descargar CSV con recursos
@recurso_bp.route("/descargar-csv")
def descargar_csv():
    csv_file = generar_csv()
    return send_file(csv_file, as_attachment=True)

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

# Función para crear backup
def crear_backup():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(current_app.config['BACKUP_FOLDER'], f"backup_{timestamp}.sql")
    os.system(f"mysqldump -u root -p gestion_sistemas > {backup_file}")
    logging.info(f"Backup creado: {backup_file}")

# Programar backup automático cada minuto
scheduler = BackgroundScheduler()
scheduler.add_job(func=crear_backup, trigger="interval", minutes=1)
scheduler.start()
