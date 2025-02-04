from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import secrets

# Inicialización de la aplicación
app = Flask(__name__)
app.config.from_object("config.Config")
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Inicialización de la base de datos
db = SQLAlchemy(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

# Inicia el programador para la copia de seguridad de la base de datos
def backup_database():
    db_path = "path_to_your_database"  # Reemplaza con la ruta real de tu base de datos
    backup_dir = "path_to_backup_folder"  # Reemplaza con la ruta real de la carpeta de respaldo
    backup_name = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    backup_path = os.path.join(backup_dir, backup_name)

    # Comando para hacer el backup (esto depende de cómo manejes tu base de datos)
    os.system(f"mysqldump -u root -p --all-databases > {backup_path}")

    print("¡Copia de seguridad realizada con éxito!")  # Reemplazo de flash()

def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_database, 'interval', hours=24)  # Ejecutar cada 24 horas
    scheduler.start()

# Llamamos a la función para iniciar el programador
init_scheduler()

# Importaciones después de inicializar app y db
from app import routes, models
