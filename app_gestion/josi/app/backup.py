import os
from datetime import datetime
from app import app, db

# Configuración
BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backups')
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# Nombre del archivo de backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_filename = f"backup_{timestamp}.sql"
backup_path = os.path.join(BACKUP_DIR, backup_filename)

# Comando para hacer el backup (usando mysqldump)
db_user = "root"  # Usuario de la base de datos
db_name = "app_gestion"  # Nombre de la base de datos
command = f"mysqldump -u {db_user} {db_name} > {backup_path}"

# Ejecutar el comando
os.system(command)

print(f"Backup creado en: {backup_path}")