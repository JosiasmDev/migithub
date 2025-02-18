import os
import csv
from fpdf import FPDF
import psutil
import logging
from datetime import datetime, timedelta
from flask import current_app
import subprocess

# ⚪️ Función para generar backup
def crear_backup():
    db_user = current_app.config['DB_USER']
    db_password = current_app.config['DB_PASSWORD']
    db_name = current_app.config['DB_NAME']
    backup_dir = current_app.config['BACKUP_FOLDER']

    os.makedirs(backup_dir, exist_ok=True)

    backup_filename = f"{db_name}_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        command = [
            "C:\\xampp\\mysql\\bin\\mysqldump.exe",
            "-u", db_user,
            f"--password={db_password}",
            db_name
        ]

        with open(backup_path, "w") as output_file:
            subprocess.run(command, stdout=output_file, check=True)

        logging.info(f"✅ Backup de la base de datos guardado en: {backup_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error en mysqldump: {e}")



# ⚪️ Función para limpiar backups antiguos
def limpiar_backups():
    now = datetime.now()
    backup_folder = current_app.config.get('BACKUP_FOLDER', 'backups')

    if not os.path.exists(backup_folder):
        logging.warning(f"⚠ La carpeta de backups no existe: {backup_folder}")
        return

    for file in os.listdir(backup_folder):
        if file.endswith(".sql"):
            try:
                file_timestamp = datetime.strptime(file.split("_backup_")[1].split(".sql")[0], "%Y-%m-%d_%H-%M-%S")
                if (now - file_timestamp) > timedelta(days=2):
                    os.remove(os.path.join(backup_folder, file))
                    logging.info(f"🗑 Backup eliminado: {file}")
            except Exception as e:
                logging.error(f"❌ Error al eliminar backup {file}: {e}")

# ⚪️ Función para generar un informe en PDF
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Recursos del Sistema", ln=True, align='C')
    
    recursos = [
        ('CPU', psutil.cpu_percent()),
        ('RAM', psutil.virtual_memory().percent),
        ('Disco', psutil.disk_usage('/').percent)
    ]
    
    for recurso, valor in recursos:
        pdf.cell(200, 10, txt=f"{recurso}: {valor}%", ln=True)
    
    reportes_folder = current_app.config.get('REPORTES_FOLDER', 'reportes_de_recursos')
    os.makedirs(reportes_folder, exist_ok=True)
    
    pdf_file = os.path.join(reportes_folder, 'recursos_report.pdf')
    pdf.output(pdf_file)
    return pdf_file

# ⚪️ Función para generar un informe en CSV
def generar_csv():
    reportes_folder = current_app.config.get('REPORTES_FOLDER', 'reportes_de_recursos')
    os.makedirs(reportes_folder, exist_ok=True)
    
    csv_file = os.path.join(reportes_folder, 'recursos_report.csv')
    
    recursos = [
        ('CPU', psutil.cpu_percent()),
        ('RAM', psutil.virtual_memory().percent),
        ('Disco', psutil.disk_usage('/').percent)
    ]
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Recurso", "Uso (%)"])
        writer.writerows(recursos)
    
    return csv_file
