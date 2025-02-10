from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import logging
import os  # Importar 'os' para manejar rutas de archivos
from apscheduler.schedulers.background import BackgroundScheduler
from logging.handlers import TimedRotatingFileHandler
import psutil  # Necesario para la obtención de recursos del sistema

# Inicializar la base de datos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar blueprint para las rutas principales
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    # Definir la carpeta de logs antes de usarla
    log_dir = os.path.join(os.path.dirname(__name__), '../logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'recursos.log')

    # Configurar los logs
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Configurar el rotado de logs (guardar logs por 7 días)
    handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7
    )
    handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(handler)

    # Función para obtener los recursos del sistema
    def obtener_recursos():
        cpu = psutil.cpu_percent(interval=1)
        memoria = psutil.virtual_memory().percent
        disco = psutil.disk_usage('/').percent
        logging.info(f'CPU: {cpu}% | Memoria: {memoria}% | Disco: {disco}%')

    # Iniciar el scheduler para ejecutar obtener_recursos cada minuto
    def iniciar_scheduler():
        scheduler = BackgroundScheduler()
        scheduler.add_job(obtener_recursos, 'interval', minutes=1)
        scheduler.start()

    iniciar_scheduler()

    

    return app

