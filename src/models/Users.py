import bcrypt
from .database import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()

    def registrar(self, usuario_data):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuario (nombre, apellido, email, password) VALUES (%s, %s, %s, %s)",
                (
                    usuario_data.nombre,
                    usuario_data.apellido,  
                    usuario_data.email,
                    usuario_data.password   
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            conn.close()

    def validar_login(self, email, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM usuario WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()

        conn.close()

        if user and bcrypt.checkpw(
            password.encode('utf-8'),
            user['password'].encode('utf-8')
        ):
            return user

        return None