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

        cursor.execute(query, valores)

        conn.commit()

        conn.close()

    def listar_grupos(self):

        conn = self.db.get_connection()

        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM grupos ORDER BY grado, grupo"

        cursor.execute(query)

        grupos = cursor.fetchall()

        conn.close()

        return grupos