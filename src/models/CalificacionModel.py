from .database import Database

class CalificacionModel:

    def __init__(self):
        self.db = Database()

    def obtener_calificaciones_alumno(self, id_alumno):

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT
            m.nombre_materia,
            c.parcial,
            c.calificacion
        FROM calificaciones c
        INNER JOIN materias m
            ON c.id_materia = m.id_materia
        WHERE c.id_alumno = %s
        ORDER BY m.nombre_materia, c.parcial
        """

        cursor.execute(query, (id_alumno,))

        datos = cursor.fetchall()

        conn.close()

        return datos