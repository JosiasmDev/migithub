# config.py - Configuración de la aplicación
import os

class Config:
    SECRET_KEY = "clave_secreta"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/gestion_sistemas"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BACKUP_FOLDER = os.path.join(os.getcwd(), 'backups')