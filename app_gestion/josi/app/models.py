from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Asegúrate de agregar estos métodos
    @property
    def is_active(self):
        # Si tu modelo tiene una columna que indica si un usuario está activo, puedes usarla aquí
        return True  # Cambia esto según tu lógica

    @property
    def is_authenticated(self):
        # Este es el comportamiento predeterminado de Flask-Login
        return True  # Puedes ajustar esto según las necesidades de tu sistema

    @property
    def is_anonymous(self):
        # Puedes dejar esto como False, ya que los usuarios autenticados no son anónimos
        return False

    def get_id(self):
        return str(self.id)