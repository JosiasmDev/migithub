from flask import Blueprint, render_template, url_for, flash, redirect
from app import db, bcrypt
from app.models.usuario_model import Usuario
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegistrationForm, LoginForm

# Blueprint de usuario
usuario_bp = Blueprint('usuario_bp', __name__)

# Ruta de Registro
@usuario_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Cifrar la contraseña
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Crear un nuevo usuario
        usuario = Usuario(nombre=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(usuario)
        db.session.commit()
        flash('Cuenta creada con éxito!', 'success')
        return redirect(url_for('usuario_bp.login'))  # Redirige al login tras el registro
    return render_template('register.html', title='Registrar', form=form)

# Ruta de Login
@usuario_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            # Al usar 'remember', la sesión será persistente
            login_user(usuario, remember=form.remember.data)
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('usuario_bp.dashboard'))  # Redirige al dashboard tras el login
        else:
            flash('Credenciales inválidas', 'danger')
    return render_template('login.html', title='Iniciar sesión', form=form)


# Ruta de Logout
@usuario_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('usuario_bp.login'))  # Redirige al login después de cerrar sesión


@usuario_bp.route("/dashboard")
@login_required
def dashboard():

    
    return render_template('dashboard.html', title='Dashboard', user=current_user)