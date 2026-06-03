from .database import Database

class CalificacionModel:

    def __init__(self):

        self.db = Database()

    def obtener_calificaciones_alumno(
        self,
        id_alumno
    ):

        conn = self.db.get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
        SELECT
            parcial,
            calificacion
        FROM calificaciones
        WHERE id_alumno = %s
        ORDER BY parcial
        """

        cursor.execute(
            query,
            (id_alumno,)
        )

        datos = cursor.fetchall()

        conn.close()

        return datos