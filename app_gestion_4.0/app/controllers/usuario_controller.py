# usuario_controller.py
from flask import Blueprint, render_template, url_for, flash, redirect, request
from app import db, bcrypt
from app.models.usuario_model import Usuario
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import RegistrationForm, LoginForm, EditUserForm

# Blueprint de usuario
usuario_bp = Blueprint('usuario_bp', __name__)

# Ruta de Registro
@usuario_bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usuario = Usuario(nombre=form.username.data, email=form.email.data, password=hashed_password, role='usuario')
        db.session.add(usuario)
        db.session.commit()
        flash('Cuenta creada con éxito!', 'success')
        return redirect(url_for('usuario_bp.login'))
    return render_template('register.html', title='Registrar', form=form)

# Ruta de Login
@usuario_bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario, remember=form.remember.data)
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('usuario_bp.dashboard'))
        else:
            flash('Credenciales inválidas', 'danger')
    return render_template('login.html', title='Iniciar sesión', form=form)

# Ruta de Logout
@usuario_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('usuario_bp.login'))

# Ruta del Dashboard
@usuario_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard', user=current_user)

# Ruta para listar usuarios
@usuario_bp.route("/usuarios")
@login_required
def ver_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/lista.html', usuarios=usuarios)

# Ruta para editar un usuario
@usuario_bp.route("/usuarios/editar/<int:id>", methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    form = EditUserForm(obj=usuario)
    if form.validate_on_submit():
        usuario.nombre = form.username.data
        usuario.email = form.email.data
        usuario.role = form.role.data
        db.session.commit()
        flash('Usuario actualizado con éxito', 'success')
        return redirect(url_for('usuario_bp.ver_usuarios'))
    return render_template('usuarios/editar.html', form=form, usuario=usuario)

# Ruta para eliminar un usuario
@usuario_bp.route("/usuarios/eliminar/<int:id>", methods=['POST'])
@login_required
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado con éxito', 'success')
    return redirect(url_for('usuario_bp.ver_usuarios'))