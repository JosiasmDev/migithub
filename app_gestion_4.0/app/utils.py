import os
import csv
import psutil
from fpdf import FPDF
from datetime import datetime
from flask import current_app  # Usamos current_app.config para acceder a la configuración de Flask


# Función para generar un PDF con los recursos
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Reporte de Recursos del Sistema", ln=True, align='C')

    # Datos de los recursos
    recursos = [
        ('CPU', psutil.cpu_percent()),
        ('RAM', psutil.virtual_memory().percent),
        ('Disco', psutil.disk_usage('/').percent)
    ]

    # Escribir los datos en el PDF
    for recurso, valor in recursos:
        pdf.cell(200, 10, txt=f"{recurso}: {valor}%", ln=True)

    # Obtener la ruta de REPORTES_FOLDER desde la configuración de Flask
    reportes_folder = current_app.config.get('REPORTES_FOLDER', 'reportes_de_recursos')  
    os.makedirs(reportes_folder, exist_ok=True)  # Asegurar que la carpeta existe

    pdf_file = os.path.join(reportes_folder, 'recursos_report.pdf')
    pdf.output(pdf_file)
    return pdf_file


# Función para generar un CSV con los recursos
def generar_csv():
    # Datos de los recursos
    recursos = [
        ('CPU', psutil.cpu_percent()),
        ('RAM', psutil.virtual_memory().percent),
        ('Disco', psutil.disk_usage('/').percent)
    ]

    # Obtener la ruta de REPORTES_FOLDER desde la configuración de Flask
    reportes_folder = current_app.config.get('REPORTES_FOLDER', 'reportes_de_recursos')
    os.makedirs(reportes_folder, exist_ok=True)  # Asegurar que la carpeta existe

    csv_file = os.path.join(reportes_folder, 'recursos_report.csv')

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Recurso", "Valor (%)"])
        for recurso, valor in recursos:
            writer.writerow([recurso, valor])

    return csv_file


def crear_backup():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = os.path.join(current_app.config['BACKUP_FOLDER'], f"backup_{timestamp}.sql")
    os.system(f"mysqldump -u root -p gestion_sistemas > {backup_file}")
    # Asegura que se registre la creación de backup en los logs
    logging.info(f"Backup creado: {backup_file}")

# Función para limpiar backups de más de 2 días
def limpiar_backups():
    now = datetime.now()
    for file in os.listdir(current_app.config['BACKUP_FOLDER']):
        if file.endswith(".sql"):
            file_path = os.path.join(current_app.config['BACKUP_FOLDER'], file)
            file_timestamp = datetime.strptime(file.split("_")[2], "%Y%m%d%H%M%S")
            if (now - file_timestamp).days > 2:
                os.remove(file_path)
