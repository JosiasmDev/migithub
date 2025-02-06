from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import User
from app import db

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/')
def index(): 
    print('raiz')
    return redirect(url_for('main.index'))

@auth_routes.route('/registro')
def registro(): 
    print('registro')
    return redirect(url_for('main.registro'))