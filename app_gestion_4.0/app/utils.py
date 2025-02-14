
# app/utils.py
import shutil
import os
from app import db
from app.models.recurso_model import Recurso
import csv
from fpdf import FPDF
from datetime import datetime

# Función para crear backup
def crear_backup():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"backups/gestion_sistemas_{timestamp}.sql"
    os.system(f"mysqldump -u root -p gestion_sistemas > {backup_file}")

# Función para limpiar backups de más de 2 días
def limpiar_backups():
    now = datetime.now()
    for file in os.listdir("backups"):
        if file.endswith(".sql"):
            file_path = os.path.join("backups", file)
            file_timestamp = datetime.strptime(file.split("_")[2], "%Y%m%d%H%M%S")
            if (now - file_timestamp).days > 2:
                os.remove(file_path)

# Función para generar un PDF con los recursos
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
    pdf.output("static/reportes/recurso_report.pdf")

# Función para generar un CSV con los recursos
def generar_csv():
    recursos = [
        ('CPU', psutil.cpu_percent()),
        ('RAM', psutil.virtual_memory().percent),
        ('Disco', psutil.disk_usage('/').percent)
    ]
    with open("static/reportes/recurso_report.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Recurso", "Valor (%)"])
        for recurso, valor in recursos:
            writer.writerow([recurso, valor])



