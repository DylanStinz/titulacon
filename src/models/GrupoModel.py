from .database import Database

class GrupoModel:

    def __init__(self):

        self.db = Database()

    def crear_grupo(
        self,
        grado,
        grupo,
        especialidad,
        turno
    ):

        conn = self.db.get_connection()

        cursor = conn.cursor()

        query = """
        INSERT INTO grupos
        (
            grado,
            grupo,
            especialidad,
            turno
        )
        VALUES (%s, %s, %s, %s)
        """

        valores = (

            grado,
            grupo,
            especialidad,
            turno

        )

        try:

            cursor.execute(query, valores)

            conn.commit()

            return True

        except Exception as e:

            print(e)

            return False

        finally:

            conn.close()

    def listar_grupos(self):

        conn = self.db.get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM grupos
        """

        cursor.execute(query)

        grupos = cursor.fetchall()

        conn.close()

        return grupos

    def obtener_alumnos_grupo(self, grupo):

        conn = self.db.get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT nombre, apellido_paterno
        FROM alumnos
        WHERE grupo = %s
        """

        cursor.execute(query, (grupo,))

        alumnos = cursor.fetchall()

        conn.close()

        return alumnos