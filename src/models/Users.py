import bcrypt
from .database import Database

class UsuarioModel:

    def __init__(self):
        self.db = Database()

    def registrar(self, usuario_data):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:

            query = """
            INSERT INTO docentes
            (
                nombre,
                apellido_paterno,
                apellido_materno,
                correo,
                usuario,
                contraseña
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            valores = (

                usuario_data.nombre,
                usuario_data.apellido_paterno,
                usuario_data.apellido_materno,
                usuario_data.correo,
                usuario_data.usuario,
                usuario_data.contraseña

            )

            cursor.execute(query, valores)

            conn.commit()

            return True

        except Exception as e:

            print(f"Error al registrar usuario: {e}")

            return False

        finally:

            conn.close()

    def validar_login(self, usuario):

        conn = self.db.get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM docentes
        WHERE usuario = %s
        """

        cursor.execute(query, (usuario,))

        user = cursor.fetchone()

        print(user)

        conn.close()

        return user