from app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='usuario')  # Roles: admin, usuario

    def __repr__(self):
        return f'<User {self.username}>'
    
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))  # Flask-Login usará esta función para cargar usuarios
