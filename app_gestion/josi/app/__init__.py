from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
numero_secreto= secrets.token_urlsafe(100)
app.secret_key=numero_secreto
if not app.secret_key:
    raise ValueError("No secret key found. Please set it in your environment variables.")  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/app_gestion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



from app import routes, models


