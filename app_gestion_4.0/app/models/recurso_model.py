from app import db

class Recurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu = db.Column(db.Float, nullable=False)
    ram = db.Column(db.Float, nullable=False)
    disco = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Recurso {self.id}>'
