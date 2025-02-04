import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "tu_clave_secreta"  # Usa la variable de entorno o una clave por defecto
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DB = "gestion_sistemas"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'  # Usa el servidor SMTP de tu proveedor de correo
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Correo electrónico
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Contraseña
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')  # Correo del remitente