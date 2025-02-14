# app/models/usuario_model.py - Modelo de usuario
class Usuario:
    def __init__(self, id, nombre, email, contraseña):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña
    
    def obtener_usuario(self, id):
        # Simulación de consulta a BD
        return Usuario(id, "Ejemplo", "ejemplo@email.com")