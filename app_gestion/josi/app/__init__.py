from flask import Flask
from app.db import db  # Importa db desde db.py, no es necesario crear una nueva instancia
import secrets
import pymysql
pymysql.install_as_MySQLdb()
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Crea la aplicación Flask
app = Flask(__name__)
numero_secreto = secrets.token_urlsafe(100)
app.secret_key = numero_secreto
if not app.secret_key:
    raise ValueError("No secret key found. Please set it in your environment variables.")

# Configura la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/app_gestion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa db con la instancia importada
db.init_app(app)

# Importa routes después de la inicialización de app
from app import routes  # Importa routes, pero no models directamente aquí

from app.models import User

def generate_users_csv():
    users = User.query.all()
    csv_filename = "users.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Username", "Email"])
        for user in users:
            writer.writerow([user.id, user.username, user.email])
    print(f"CSV generado: {csv_filename}")

def generate_users_pdf():
    users = User.query.all()
    pdf_filename = "users.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    y = 750  # Posición inicial en el PDF

    c.drawString(50, y, "Lista de Usuarios")
    y -= 20

    for user in users:
        c.drawString(50, y, f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
