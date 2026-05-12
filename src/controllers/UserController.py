import bcrypt
from models.Users import UsuarioModel
from models.schemasModel import UsuarioSchema
from pydantic import ValidationError

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()
        
    def registrar_usuario(self, nombre, apellido, email, password):
        try:
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            nuevo_usuario = UsuarioSchema(
                nombre=nombre,
                apellido=apellido,
                email=email,
                password=hashed_password
            )

            success = self.model.registrar(nuevo_usuario)
            return success, "Usuario registrado exitosamente." 

        except ValidationError as e:
            return False, e.errors()[0]['msg']

    def login(self, email, password):
        user = self.model.validar_login(email, password)
        
        if not user:
            return None, "Credenciales incorrectas"

       
        usuario = {
            "id": user["id_usuario"],  
            "nombre": user["nombre"],
            "email": user["email"]
        }

        return usuario, "Login exitoso"