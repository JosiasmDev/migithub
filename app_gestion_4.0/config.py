import os

class Config:
    SECRET_KEY = "clave_secreta"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/gestion_sistemas"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Definimos las rutas de las carpetas
    BASE_DIR = os.getcwd()  # Directorio base de la aplicación
    BACKUP_FOLDER = os.path.join(BASE_DIR, 'backups')
    LOG_FOLDER = os.path.join(BASE_DIR, 'logs') 
    REPORTES_FOLDER = os.path.join(BASE_DIR, 'reportes_de_recursos')

    # Configuración de la base de datos para el backup
    DB_USER = "root"
    DB_PASSWORD = ""  # Si tienes contraseña, colócala aquí
    DB_NAME = "gestion_sistemas"

    # Crear las carpetas si no existen
    for folder in [BACKUP_FOLDER, LOG_FOLDER, REPORTES_FOLDER]:
        os.makedirs(folder, exist_ok=True)