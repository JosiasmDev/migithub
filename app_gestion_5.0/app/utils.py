import psutil
from datetime import datetime
from app import db
from app.models.recurso_model import Recurso

def obtener_recursos():
    recursos = []
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    fecha = datetime.now()

    recursos.append(Recurso(tipo="CPU", valor=cpu, fecha=fecha))
    recursos.append(Recurso(tipo="RAM", valor=ram, fecha=fecha))
    recursos.append(Recurso(tipo="Disco", valor=disk, fecha=fecha))

    db.session.add_all(recursos)
    db.session.commit()

    return recursos
