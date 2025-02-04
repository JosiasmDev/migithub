# formulario de registro
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmar contraseña", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Registrarse")

    def validate_username(self, username):
        """Verifica si el nombre de usuario ya existe en la base de datos."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Ese nombre de usuario ya está en uso. Por favor, elige otro.")

    def validate_email(self, email):
        """Verifica si el correo ya está registrado."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Ese correo electrónico ya está en uso. Prueba con otro.")

class LoginForm(FlaskForm):
    email = StringField("Correo electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    remember = BooleanField("Recordarme")  # Permite mantener la sesión iniciada
    submit = SubmitField("Iniciar sesión")
