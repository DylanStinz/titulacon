import bcrypt
from models.Users import UsuarioModel
from models.schemasModel import UsuarioSchema
from pydantic import ValidationError

class AuthController:

    def __init__(self):
        self.model = UsuarioModel()


    def registrar_usuario(
        self,
        nombre,
        apellido_paterno,
        apellido_materno,
        correo,
        usuario,
        password
    ):

        try:

            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")

            nuevo_usuario = UsuarioSchema(

                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                correo=correo,
                usuario=usuario,
                contraseña=hashed_password
            )

            success = self.model.registrar(nuevo_usuario)

            if success:
                return True, "Usuario registrado correctamente"

            return False, "No se pudo registrar"

        except ValidationError as e:
            return False, e.errors()[0]["msg"]

        except Exception as e:
            return False, str(e)

    def login(self, usuario, password):

        user = self.model.validar_login(usuario)

        if not user:

            return None, "Usuario incorrecto"

        if not bcrypt.checkpw(

            password.encode("utf-8"),
            user["contraseña"].encode("utf-8")

        ):

            return None, "Contraseña incorrecta"

        usuario_data = {

            "id": user["id_docente"],
            "nombre": user["nombre"],
            "correo": user["correo"],
            "usuario": user["usuario"]

        }

        return usuario_data, "Login exitoso"