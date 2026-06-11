from .database import Database

class ReporteModel:

    def __init__(self):
        self.db = Database()

    def listar_reportes_por_docente(self, id_docente):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT r.*
            FROM reportes r
            WHERE r.id_docente = %s
            ORDER BY r.fecha_generado DESC
        """

        cursor.execute(query, (id_docente,))
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data

    def obtener_reporte_por_id(self, id_reporte):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM reportes WHERE id_reporte = %s"
        cursor.execute(query, (id_reporte,))

        reporte = cursor.fetchone()

        cursor.close()
        conn.close()
        return reporte

    def crear_reporte(self, id_docente, tipo_reporte, descripcion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO reportes (id_docente, tipo_reporte, descripcion)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (id_docente, tipo_reporte, descripcion))
        conn.commit()

        last_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return last_id

    def actualizar_reporte(self, id_reporte, tipo_reporte, descripcion):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE reportes 
            SET tipo_reporte = %s, descripcion = %s
            WHERE id_reporte = %s
        """

        cursor.execute(query, (tipo_reporte, descripcion, id_reporte))
        conn.commit()

        cursor.close()
        conn.close()

        return True

    def eliminar_reporte(self, id_reporte):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM reportes WHERE id_reporte = %s", (id_reporte,))
        conn.commit()

        cursor.close()
        conn.close()

        return True