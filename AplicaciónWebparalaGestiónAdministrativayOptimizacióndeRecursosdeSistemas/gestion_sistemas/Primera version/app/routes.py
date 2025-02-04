from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import psutil

# Ruta de registro de usuario
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash de la contraseña
        hashed_password = generate_password_hash(form.password.data, method="pbkdf2:sha256")
        # Crear nuevo usuario
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("¡Registro exitoso! Por favor inicia sesión.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Formulario de login
    if form.validate_on_submit():
        # Busca el usuario por el email
        user = User.query.filter_by(email=form.email.data).first()
        
        # Verifica si el usuario existe y si la contraseña es correcta
        if user and check_password_hash(user.password, form.password.data):
            # Si las credenciales son correctas, se inicia la sesión
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("home"))
        else:
            # Si las credenciales son incorrectas, se muestra un mensaje de error
            flash("Usuario o contraseña incorrectos", "danger")
    
    return render_template("login.html", form=form)


# Ruta de inicio (Home)
@app.route("/home")
@login_required  # Requiere que el usuario esté autenticado
def home():
    return render_template("home.html")

# Ruta para cerrar sesión
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for("login"))

# Ruta para monitorear el sistema
@app.route("/monitor")
@login_required
def monitor():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')

    system_data = {
        "cpu_percent": cpu_percent,
        "memory_percent": memory_info.percent,
        "memory_used_gb": round(memory_info.used / (1024 ** 3), 2),
        "memory_total_gb": round(memory_info.total / (1024 ** 3), 2),
        "disk_percent": disk_usage.percent,
        "disk_used_gb": round(disk_usage.used / (1024 ** 3), 2),
        "disk_total_gb": round(disk_usage.total / (1024 ** 3), 2),
    }

    return render_template("monitor.html", system_data=system_data)

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
