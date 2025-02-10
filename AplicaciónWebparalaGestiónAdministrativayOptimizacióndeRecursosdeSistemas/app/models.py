from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Almacenamos la contraseña en texto plano
    role = db.Column(db.String(20), nullable=False, default='usuario')  # Roles: admin, usuario

    def __repr__(self):
        return f'<User {self.username}>'
    
def obtener_datos_rendimiento():
    # Simulación de datos; reemplázalo con una consulta a la base de datos.
    datos = [
        {'nombre': 'Uso de CPU', 'valor': '45%'},
        {'nombre': 'Uso de Memoria', 'valor': '3.2 GB'},
        {'nombre': 'Tiempo de Respuesta', 'valor': '120 ms'}
    ]
    return datos