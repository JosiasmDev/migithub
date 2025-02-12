from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import os
from apscheduler.schedulers.background import BackgroundScheduler
from logging.handlers import TimedRotatingFileHandler
import psutil
from datetime import datetime
from flask import session



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

    @app.context_processor
    def inject_usuario():
        return dict(usuario=session.get('usuario'))

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

    # Función para realizar el backup de la base de datos
    def backup_db():
        # Configura los parámetros de tu base de datos
        db_user = app.config['DB_USER']
        db_password = app.config['DB_PASSWORD']
        db_name = app.config['DB_NAME']
        backup_dir = app.config['BACKUP_DIR']

        # Define el nombre del archivo de backup
        backup_filename = f"{db_name}_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
        backup_path = os.path.join(backup_dir, backup_filename)

        # Comando mysqldump
        dump_command = f"C:\\xampp\\mysql\\bin\\mysqldump -u {db_user} {db_name} > {backup_path}"


        # Ejecuta el comando
        os.system(dump_command)
        print(f"Backup de la base de datos completado: {backup_path}")

    # Iniciar el scheduler
    scheduler = BackgroundScheduler()

    # Programar las tareas: obtener recursos cada minuto y backup cada minuto
    scheduler.add_job(obtener_recursos, 'interval', hours=1)
    scheduler.add_job(backup_db, 'interval', hours=1)

    # Iniciar el scheduler
    scheduler.start()

    # Importa las rutas después de definir la app
    from . import routes

    return app
