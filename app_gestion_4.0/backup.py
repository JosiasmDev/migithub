# backup.py

import os
from datetime import datetime
import subprocess
import time
from config import *  # Asegúrate de que estos valores estén definidos en el archivo config.py

# Configuración
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "gestion_sistemas"
BACKUP_FOLDER = "backups"
INTERVALO_SEGUNDOS = 3600  # Intervalo en segundos entre cada backup

# Crear carpeta de backups si no existe
if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

def hacer_backup():
    """Función para generar un backup de la base de datos."""
    db_user = DB_USER
    db_password = DB_PASSWORD
    db_name = DB_NAME
    backup_dir = BACKUP_FOLDER

    os.makedirs(backup_dir, exist_ok=True)

    # Nombre del archivo de backup con fecha y hora
    backup_filename = f"{db_name}_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)

    # Comando para hacer el backup
    command = [
        "C:\\xampp\\mysql\\bin\\mysqldump.exe",
        "-u", db_user,
        f"--password={db_password}",
        db_name,
        "-r", backup_path  # Redirige la salida a un archivo .sql
    ]

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"[{datetime.now()}] Backup exitoso: {backup_path}")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] Error al hacer el backup: {e}")

def iniciar_backup_automatico():
    """Ejecuta backups automáticamente cada cierto tiempo."""
    while True:
        hacer_backup()
        time.sleep(INTERVALO_SEGUNDOS)  # Esperar el intervalo definido antes de hacer otro backup

# Comentado el hilo aquí, ya no es necesario
# backup_thread = threading.Thread(target=iniciar_backup_automatico, daemon=True)
# backup_thread.start()
