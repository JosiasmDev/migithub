import psutil

def get_system_usage():
    # Obtener el uso de CPU
    cpu_percent = psutil.cpu_percent(interval=1)

    # Obtener el uso de memoria
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent

    # Obtener el uso de almacenamiento
    disk_usage = psutil.disk_usage('/')
    disk_percent = disk_usage.percent

    return {
        'cpu_percent': cpu_percent,
        'memory_percent': memory_percent,
        'disk_percent': disk_percent
    }


def check_system_usage():
    usage = get_system_usage()
    alerts = []

    if usage['cpu_percent'] > 80:
        alerts.append(f"Uso de CPU alto: {usage['cpu_percent']}%")
    if usage['memory_percent'] > 80:
        alerts.append(f"Uso de memoria alto: {usage['memory_percent']}%")
    if usage['disk_percent'] > 80:
        alerts.append(f"Uso de almacenamiento alto: {usage['disk_percent']}%")

    return alerts

