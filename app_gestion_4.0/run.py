# run.py - Punto de entrada de la aplicación
from app import create_app
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app)

if __name__ == "__main__":
    app.run(debug=True)