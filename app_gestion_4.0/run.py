# run.py - Punto de entrada de la aplicación
from app import create_app
from flask_migrate import Migrate
from app.controllers.recurso_controller import iniciar_scheduler

app = create_app()
migrate = Migrate(app)

# Iniciar programador de tareas
iniciar_scheduler(app)

if __name__ == "__main__":
    app.run(debug=True)
