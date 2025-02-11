from flask import Blueprint, render_template, redirect, url_for, flash, request, session, send_file, jsonify, current_app
from app.models import User
from app import db
from app.tools.system_monitor import get_system_usage, check_system_usage
import os
from datetime import datetime  # Importar datetime
from .tools.informes import generar_informe_pdf, generar_informe_csv
from .models import obtener_datos_rendimiento
from datetime import datetime

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index(): 
    print(session.get('username', 'Usuario'))
    username = session.get('username', 'Usuario')  # Si no hay sesión, muestra 'Usuario' por defecto
    return render_template('index.html', username=username)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username  # Guardamos el nombre del usuario en la sesión
        print(session['username'])
        if not username or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('main.login'))
        
        # Buscar al usuario por nombre de usuario
        user = User.query.filter_by(username=username).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user and user.password == password:
            flash('¡Bienvenido de nuevo!', 'success')
            return redirect(url_for('main.index'))  # Redirige al inicio o donde quieras
        else:
            flash('Credenciales incorrectas, intenta de nuevo.', 'danger')
    
    return render_template('login.html')

@main_routes.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@main_routes.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    # Obtener el usuario de la base de datos
    usuario = User.query.get_or_404(id)

    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')

        # Validar que los campos no estén vacíos
        if not username or not email or not role:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('editar_usuario.html', usuario=usuario)

        # Actualizar el usuario
        usuario.username = username
        usuario.email = email
        usuario.role = role

        try:
            db.session.commit()  # Guardar cambios en la base de datos
            flash('Usuario actualizado correctamente', 'success')
            return redirect(url_for('main.listar_usuarios'))  # Redirigir a la lista de usuarios
        except Exception as e:
            db.session.rollback()  # En caso de error, deshacer cambios
            flash('Error al actualizar el usuario: ' + str(e), 'danger')
            
    return render_template('editar_usuario.html', usuario=usuario)

@main_routes.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('main.listar_usuarios'))  # Redirigir a la lista actualizada

@main_routes.route('/monitoreo')
def monitoreo():
    print('monitoreo')
    system_usage = get_system_usage()
    alerts = check_system_usage()
    return render_template('monitoreo.html', system_usage=system_usage, alerts=alerts)

@main_routes.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('main.registro'))
        
        # Verificar que no exista un usuario con el mismo nombre de usuario o correo
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('El nombre de usuario o correo ya está en uso.', 'danger')
            return redirect(url_for('main.registro'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario registrado correctamente.', 'success')
        return redirect(url_for('main.index'))  # Redirige a la página principal después del registro
    
    return render_template('registro.html')

@main_routes.route('/logs')
def ver_logs():
    log_file = os.path.join(os.path.dirname(__file__), '../logs/recursos.log')

    try:
        with open(log_file, 'r') as f:
            logs = f.readlines()
    except FileNotFoundError:
        logs = ["No se encuentran logs disponibles"]

    # Agrupar logs por fecha
    logs_grouped_by_day = {}

    for log in logs:
        try:
            timestamp = log.split(" - ")[0]
            log_datetime = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            day = log_datetime.date()

            if day not in logs_grouped_by_day:
                logs_grouped_by_day[day] = []

            logs_grouped_by_day[day].append(log)

        except ValueError:
            continue

    return render_template('logs.html', logs_grouped_by_day=logs_grouped_by_day)


@main_routes.route('/descargar_pdf')
def descargar_pdf():
    datos = obtener_datos_rendimiento()
    filename = 'informe.pdf'
    ruta_archivo = os.path.join(current_app.root_path, filename)  # Elimina el duplicado 'app'
    generar_informe_pdf(datos, ruta_archivo)
    return send_file(ruta_archivo, as_attachment=True)

@main_routes.route('/descargar_csv')
def descargar_csv():
    datos = obtener_datos_rendimiento()
    filename = 'informe.csv'
    ruta_archivo = os.path.join(current_app.root_path, filename)  # Igualmente para el CSV
    generar_informe_csv(datos, ruta_archivo)
    return send_file(ruta_archivo, as_attachment=True)


# Ruta principal donde se muestra el botón de backup
@main_routes.route('/backup')
def backup_page():
    return render_template('backup.html')

# Ruta para forzar el backup
@main_routes.route('/force_backup')
def force_backup():
    # Llama a la función de backup directamente
    backup_db(current_app)
    return redirect(url_for('main.backup_page'))  # Redirige de nuevo a la página del backup

# Función para realizar el backup de la base de datos
def backup_db(app):
    # Configura los parámetros de tu base de datos
    db_user = app.config['DB_USER']
    db_password = app.config['DB_PASSWORD']
    db_name = app.config['DB_NAME']
    backup_dir = app.config['BACKUP_DIR']

    # Define el nombre del archivo de backup
    backup_filename = f"{db_name}_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)

    # Comando mysqldump
    dump_command = f"mysqldump -u {db_user} -p{db_password} {db_name} > {backup_path}"

    # Ejecuta el comando
    os.system(dump_command)
    print(f"Backup de la base de datos completado: {backup_path}")
