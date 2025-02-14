from flask import render_template, redirect, url_for, request, flash, send_file, send_from_directory
from app import app, DOWNLOADS_DIR
from app.models import User
from passlib.hash import scrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from passlib.hash import scrypt
from app.db import db
import os

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and scrypt.verify(password, user.password):  # Verificar con scrypt
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = scrypt.hash(request.form['password'])  # Hashear con scrypt
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('El usuario o el email ya existen')
            return redirect(url_for('register'))
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado con éxito')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/generate_csv')
@login_required
def generate_csv():
    generate_users_csv()
    return send_from_directory(directory=DOWNLOADS_DIR, path="users.csv", as_attachment=True)

@app.route('/generate_pdf')
@login_required
def generate_pdf():
    generate_users_pdf()
    return send_from_directory(directory=DOWNLOADS_DIR, path="users.pdf", as_attachment=True)

@app.route('/download/pdf')
def download_pdf():
    return send_from_directory(directory=DOWNLOADS_DIR, path="resources.pdf", as_attachment=True)

@app.route('/download/csv')
def download_csv():
    return send_from_directory(directory=DOWNLOADS_DIR, path="resources.csv", as_attachment=True)
