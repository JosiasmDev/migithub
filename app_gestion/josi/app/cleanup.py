import os
import time
from datetime import datetime, timedelta

# Configuración
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')
LOGS_DIR = os.path.join(os.path.dirname(__file__), 'logs')

# Días de antigüedad para eliminar
DAYS_TO_KEEP = 10  # Para logs
BACKUP_DAYS_TO_KEEP = 3  # Para backups

def delete_old_files(directory, days_to_keep):
    now = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > days_to_keep * 86400:  # 86400 segundos = 1 día
                os.remove(file_path)
                print(f"Eliminado: {file_path}")

# Eliminar logs antiguos
if os.path.exists(LOGS_DIR):
    delete_old_files(LOGS_DIR, DAYS_TO_KEEP)

# Eliminar backups antiguos
if os.path.exists(BACKUP_DIR):
    delete_old_files(BACKUP_DIR, BACKUP_DAYS_TO_KEEP)

print("Limpieza completada.")