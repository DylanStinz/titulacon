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
        SELECT AVG(
            CASE
                WHEN calificacion > 10 THEN 10
                ELSE calificacion
            END
        )
        FROM calificaciones
        WHERE calificacion > 0
        """)

        promedio = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return round(promedio or 0, 2)

    def total_aprobados(self):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM (
            SELECT
                id_alumno,
                AVG(
                    CASE
                        WHEN calificacion > 10 THEN 10
                        ELSE calificacion
                    END
                ) AS promedio
            FROM calificaciones
            WHERE calificacion > 0
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
            SELECT
                id_alumno,
                AVG(
                    CASE
                        WHEN calificacion > 10 THEN 10
                        ELSE calificacion
                    END
                ) AS promedio
            FROM calificaciones
            WHERE calificacion > 0
            GROUP BY id_alumno
            HAVING promedio < 6
        ) AS alumnos_reprobados
        """

        cursor.execute(query)

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total