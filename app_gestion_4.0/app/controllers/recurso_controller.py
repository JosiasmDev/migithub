from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, current_app, send_file
import psutil
import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import ConflictingIdError
import app.utils as utils

recurso_bp = Blueprint('recurso_bp', __name__)

# 🔹 Programador de tareas con APScheduler (Definir solo una vez)
scheduler = BackgroundScheduler()

def iniciar_scheduler(app):
    with app.app_context():
        try:
            if not scheduler.running:
                logging.info("🕒 Iniciando scheduler...")
                scheduler.add_job(func=monitorizar_recursos, trigger="interval", seconds=30, id="monitor", replace_existing=True)
                scheduler.add_job(func=backup_automatico, trigger="interval", seconds=10, id="backup", replace_existing=True)
                scheduler.start()
        except ConflictingIdError:
            logging.error("❌ Error de conflicto de ID en el scheduler.")
        except Exception as e:
            logging.error(f"❌ Error al iniciar el scheduler: {e}")

# 🔹 Configurar logs
def configurar_logging():
    log_folder = current_app.config['LOG_FOLDER']
    os.makedirs(log_folder, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_folder, 'recursos.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# 🔹 Función de monitoreo de recursos
def monitorizar_recursos():
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        logging.info(f"📊 CPU: {cpu}%, RAM: {memory}%, Disco: {disk}%")
    except Exception as e:
        logging.error(f"❌ Error al monitorizar recursos: {e}")

# 🔹 Función para ejecutar backups automáticos
'''def backup_automatico():
    try:
        logging.info("🕒 Iniciando backup automático...")
        utils.crear_backup()  # Asegúrate de que esta función esté bien implementada
        logging.info("✅ Backup automático realizado correctamente.")
    except Exception as e:
        logging.error(f"❌ Error en el backup automático: {e}")
'''
        
# 🔹 Ruta para forzar backup manual
@recurso_bp.route("/forzar-backup")
def forzar_backup():
    try:
        utils.crear_backup()
        flash('✅ Backup realizado con éxito', 'success')
    except Exception as e:
        flash(f'❌ Error al realizar el backup: {e}', 'danger')
    return redirect(url_for('usuario_bp.dashboard'))

# 🔹 Ruta para ver logs
@recurso_bp.route("/logs")
def ver_logs():
    log_file = os.path.join(current_app.config['LOG_FOLDER'], 'recursos.log')
    if not os.path.exists(log_file):
        flash("⚠ No hay logs disponibles", "warning")
        return redirect(url_for('recurso_bp.ver_recursos'))
    
    with open(log_file, 'r') as f:
        logs = f.readlines()
    return render_template('recurso/logs.html', logs=logs)

# 🔹 Ruta para descargar reporte en PDF
@recurso_bp.route("/descargar-pdf")
def descargar_pdf():
    try:
        pdf_file = utils.generar_pdf()
        if os.path.exists(pdf_file):
            return send_file(pdf_file, as_attachment=True)
        else:
            flash("⚠ El archivo PDF no se generó correctamente", "danger")
    except Exception as e:
        flash(f"❌ Error al generar el PDF: {e}", "danger")
    return redirect(url_for('recurso_bp.ver_recursos'))

# 🔹 Ruta para descargar reporte en CSV
@recurso_bp.route("/descargar-csv")
def descargar_csv():
    try:
        csv_file = utils.generar_csv()  # Corregido el error tipográfico
        if os.path.exists(csv_file):
            return send_file(csv_file, as_attachment=True)
        else:
            flash("⚠ El archivo CSV no se generó correctamente", "danger")
    except Exception as e:
        flash(f"❌ Error al generar el CSV: {e}", "danger")
    return redirect(url_for('recurso_bp.ver_recursos'))

# 🔹 Ruta para ver recursos
@recurso_bp.route("/recursos")
def ver_recursos():
    recursos = {
        'cpu': psutil.cpu_percent(),
        'ram': psutil.virtual_memory().percent,
        'disco': psutil.disk_usage('/').percent
    }
    return render_template('recurso/lista.html', recursos=recursos)

# 🔹 Ruta para limpiar backups antiguos
@recurso_bp.route("/limpiar-backups")
def limpiar_backups_route():
    try:
        utils.limpiar_backups()
        flash('✅ Backups limpiados con éxito', 'success')
    except Exception as e:
        flash(f'❌ Error al limpiar los backups: {e}', 'danger')
    return redirect(url_for('recurso_bp.ver_recursos'))

# 🔹 Ruta para obtener recursos en JSON
@recurso_bp.route("/recursos_json")
def obtener_recursos_json():
    recursos = {
        'cpu': psutil.cpu_percent(interval=1),
        'ram': psutil.virtual_memory().percent,
        'disco': psutil.disk_usage('/').percent
    }
    return jsonify(recursos)