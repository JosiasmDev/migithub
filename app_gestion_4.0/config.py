# config.py - Configuración de la aplicación
class Config:
    SECRET_KEY = "clave_secreta"
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/gestion_sistemas"
    SQLALCHEMY_TRACK_MODIFICATIONS = False