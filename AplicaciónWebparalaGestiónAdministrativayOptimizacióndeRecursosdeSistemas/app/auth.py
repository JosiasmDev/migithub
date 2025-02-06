from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('El correo electrónico ya está registrado.', 'error')
            return redirect(url_for('auth.registro'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Por favor, inicia sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('registro.html')

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Correo electrónico o contraseña incorrectos.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        print(f"Usuario autenticado: {user.username}")  # Mensaje de depuración
        return redirect(url_for('main.index'))

    return render_template('login.html')

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))