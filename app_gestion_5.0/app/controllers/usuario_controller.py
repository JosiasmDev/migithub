from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import db
from app.models.usuario_model import Usuario
from app.forms import LoginForm, RegisterForm

# Definir el blueprint correctamente
bp = Blueprint('usuario', __name__)

@bp.route('/')
def index():
    return redirect(url_for('usuario.login'))  # Redirige a la página de login

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.password.data):
            login_user(usuario)
            flash('Login exitoso', 'success')
            return redirect(url_for('recurso.dashboard'))
        flash('Correo o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('usuario.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        usuario = Usuario(username=form.username.data, email=form.email.data)
        usuario.set_password(form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('usuario.login'))
    return render_template('register.html', form=form)
