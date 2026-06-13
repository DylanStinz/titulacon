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
    def actualizar_calificacion(self, id_alumno, parcial, nueva_calificacion):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya existe la calificación
        query_check = "SELECT id_calificacion FROM calificaciones WHERE id_alumno = %s AND parcial = %s"
        cursor.execute(query_check, (id_alumno, parcial))
        existe = cursor.fetchone()
        
        if existe:
            query = "UPDATE calificaciones SET calificacion = %s WHERE id_alumno = %s AND parcial = %s"
            cursor.execute(query, (nueva_calificacion, id_alumno, parcial))
        else:
            query = """
            INSERT INTO calificaciones (id_alumno, parcial, calificacion, fecha_registro)
            VALUES (%s, %s, %s, CURDATE())
            """
            cursor.execute(query, (id_alumno, parcial, nueva_calificacion))
        
        conn.commit()
        cursor.close()
        conn.close()