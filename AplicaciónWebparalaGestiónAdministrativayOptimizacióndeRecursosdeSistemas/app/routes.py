from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User
from app.utils.system_monitor import get_system_usage, check_system_usage

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
@login_required
def index(): 
    print(f"Usuario actual: {current_user.username}")  # Mensaje de depuración
    return render_template('index.html')

@main_routes.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'error')
        return redirect(url_for('main.index'))

    usuarios = User.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@main_routes.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if current_user.role != 'admin':
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('main.index'))

    usuario = User.query.get_or_404(id)

    if request.method == 'POST':
        usuario.username = request.form.get('username')
        usuario.email = request.form.get('email')
        usuario.role = request.form.get('role')
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('main.listar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@main_routes.route('/usuarios/eliminar/<int:id>')
@login_required
def eliminar_usuario(id):
    if current_user.role != 'admin':
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('main.index'))

    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('main.listar_usuarios'))

@main_routes.route('/monitoreo')
@login_required
def monitoreo():
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página.', 'error')
        return redirect(url_for('main.index'))

    system_usage = get_system_usage()
    alerts = check_system_usage()
    return render_template('monitoreo.html', system_usage=system_usage, alerts=alerts)