from flask import Flask
from app.db import db
import secrets
import pymysql
pymysql.install_as_MySQLdb()
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime
from app.models import *

# Crea la aplicación Flask
app = Flask(__name__)
numero_secreto = secrets.token_urlsafe(100)
app.secret_key = numero_secreto
if not app.secret_key:
    raise ValueError("No secret key found. Please set it in your environment variables.")

DOWNLOADS_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

# Configura la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/app_gestion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa db con la instancia importada
db.init_app(app)

# Importa routes después de la inicialización de app
from app import routes  # Importa routes, pero no models directamente aquí

from app.models import User

# Función para generar PDF de usuarios
def generate_users_pdf():
    users = User.query.all()
    pdf_filename = os.path.join(DOWNLOADS_DIR, "users.pdf")
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    y = 750  # Posición inicial en el PDF

    c.drawString(50, y, "Lista de Usuarios")
    y -= 20

    for user in users:
        c.drawString(50, y, f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
        y -= 20
        if y < 50:  # Si se acaba el espacio, crea una nueva página
            c.showPage()
            y = 750

    c.save()
    print(f"PDF generado: {pdf_filename}")

# Función para generar CSV de usuarios
def generate_users_csv():
    users = User.query.all()
    csv_filename = os.path.join(DOWNLOADS_DIR, "users.csv")
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Username", "Email"])
        for user in users:
            writer.writerow([user.id, user.username, user.email])
    print(f"CSV generado: {csv_filename}")

# Funciones para generar PDF y CSV de recursos
from app.models import Resource

def generate_resources_pdf():
    print("Generando PDF de recursos...")  # Verifica que se llame la función
    pdf_filename = os.path.join(DOWNLOADS_DIR, 'resources.pdf')
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    y = 750

    resources = Resource.query.all()
    c.drawString(50, y, "Lista de Recursos del Sistema")
    y -= 20

    for resource in resources:
        c.drawString(50, y, f"ID: {resource.id}, Recurso: {resource.name}, Uso: {resource.usage}%, Estado: {resource.status}, Fecha: {resource.timestamp}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750

    c.save()
    print(f"PDF generado: {pdf_filename}")


def generate_resources_csv():
    csv_filename = os.path.join(DOWNLOADS_DIR, 'resources.csv')
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Recurso", "Uso (%)", "Estado", "Fecha"])
        for resource in Resource.query.all():
            writer.writerow([resource.id, resource.name, resource.usage, resource.status, resource.timestamp])
    print(f"CSV generado: {csv_filename}")
