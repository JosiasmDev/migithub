import os
import shutil
from datetime import datetime

def backup_db():
    db_file = 'gestion_sistemas.db'
    backup_folder = 'backups'
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_folder, f'backup_{timestamp}.db')
    shutil.copy(db_file, backup_file)
