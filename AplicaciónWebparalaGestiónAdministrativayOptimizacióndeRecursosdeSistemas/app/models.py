from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Almacenamos la contraseña en texto plano
    role = db.Column(db.String(20), nullable=False, default='usuario')  # Roles: admin, usuario

    def __repr__(self):
        return f'<User {self.username}>'