import os

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/gestion_sistemas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clave secreta para sesiones de Flask
    SECRET_KEY = 'tu_clave_secreta_aqui'