import os

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/gestion_sistemas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta para sesiones de Flask
    SECRET_KEY = 'tu_clave_secreta_aqui'

    # Configuración de la base de datos
    DB_USER = 'root'
    DB_PASSWORD = ''
    DB_NAME = 'gestion_sistemas'
    
    # Directorio para guardar los backups
    BACKUP_DIR = 'C:/xampp/htdocs/xampp/migithub/AplicaciónWebparalaGestiónAdministrativayOptimizacióndeRecursosdeSistemas/backups'
