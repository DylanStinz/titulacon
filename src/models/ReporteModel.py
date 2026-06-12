from .database import Database

class ReporteModel:

    def __init__(self):
        self.db = Database()

    # ========== MÉTODOS ORIGINALES (para compatibilidad con docentes) ==========
    def listar_reportes_por_docente(self, id_docente):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT r.*, a.nombre as alumno_nombre, a.apellido_paterno
            FROM reportes r
            LEFT JOIN alumnos a ON r.id_alumno = a.id_alumno
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

    # ========== NUEVOS MÉTODOS PARA REPORTES POR ALUMNO ==========
    def listar_reportes_por_alumno(self, id_alumno):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM reportes
            WHERE id_alumno = %s
            ORDER BY fecha_generado DESC
        """
        cursor.execute(query, (id_alumno,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def crear_reporte_con_titulo(self, id_alumno, id_docente, titulo, descripcion, tipo_reporte, estado):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO reportes (id_alumno, id_docente, titulo, descripcion, tipo_reporte, estado, fecha_generado)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (id_alumno, id_docente, titulo, descripcion, tipo_reporte, estado))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    def actualizar_reporte_completo(self, id_reporte, titulo, descripcion, tipo_reporte, estado):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
            UPDATE reportes 
            SET titulo = %s, descripcion = %s, tipo_reporte = %s, estado = %s
            WHERE id_reporte = %s
        """
        cursor.execute(query, (titulo, descripcion, tipo_reporte, estado, id_reporte))
        conn.commit()
        cursor.close()
        conn.close()
        return True
        