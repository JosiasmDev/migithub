from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import User
from app import db
from app.utils.system_monitor import get_system_usage, check_system_usage

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index(): 
    print('raiz')
    return render_template('index.html')

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
        except Exception as e:
            db.session.rollback()  # En caso de error, deshacer cambios
            flash('Error al actualizar el usuario: ' + str(e), 'danger')
            
    return render_template('editar_usuario.html', usuario=usuario)

        #return redirect(url_for('main.usuarios'))  # Redirigir a la lista de usuarios

    #return render_template('editar_usuario.html', usuario=usuario)

@main_routes.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('main.usuarios'))  # Redirigir a la lista actualizada


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

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

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
