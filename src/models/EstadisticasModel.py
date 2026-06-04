from .database import Database

class EstadisticasModel:

    def __init__(self):

        self.db = Database()

    def total_alumnos(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM alumnos"
        )

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    def promedio_general(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT AVG(calificacion)
        FROM calificaciones
        """)

        promedio = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return round(promedio or 0, 2)

    def total_aprobados(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(DISTINCT id_alumno)
        FROM calificaciones
        WHERE calificacion >= 6
        """)

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    def total_reprobados(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(DISTINCT id_alumno)
        FROM calificaciones
        WHERE calificacion < 6
        """)

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total
    def total_aprobados(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM (
            SELECT id_alumno,
                AVG(calificacion) AS promedio
            FROM calificaciones
            GROUP BY id_alumno
            HAVING promedio >= 6
        ) AS alumnos_aprobados
        """

        cursor.execute(query)

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    def total_reprobados(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM (
            SELECT id_alumno,
                AVG(calificacion) AS promedio
            FROM calificaciones
            GROUP BY id_alumno
            HAVING promedio < 6
        ) AS alumnos_reprobados
        """

        cursor.execute(query)

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total