from .database import Database

class ReporteModel:

    def __init__(self):
        self.db = Database()

    def listar_reportes_por_alumno(self, id_alumno):
        """Lista todos los reportes de un alumno específico"""
        query = """
            SELECT r.*, 
                CONCAT(a.nombre, ' ', a.apellido_paterno, ' ', a.apellido_materno) AS alumno_nombre
            FROM reportes r
            INNER JOIN alumnos a ON r.id_alumno = a.id_alumno
            WHERE r.id_alumno = %s
            ORDER BY r.fecha_creacion DESC
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (id_alumno,))
        return cursor.fetchall()

    def obtener_reporte_por_id(self, id_reporte):
        """Obtiene un reporte por su ID"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM reportes WHERE id_reporte = %s"
        cursor.execute(query, (id_reporte,))
        reporte = cursor.fetchone()
        cursor.close()
        conn.close()
        return reporte

    def crear_reporte(self, id_alumno, titulo, descripcion, tipo_reporte, estado):
        """Crea un nuevo reporte para un alumno"""
        query = """
            INSERT INTO reportes (id_alumno, titulo, descripcion, tipo_reporte, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor = self.connection.cursor()
        cursor.execute(query, (id_alumno, titulo, descripcion, tipo_reporte, estado))
        self.connection.commit()
        return cursor.lastrowid

    def actualizar_reporte(self, id_reporte, titulo, descripcion, tipo_reporte, estado):
        """Actualiza un reporte existente"""
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

    def eliminar_reporte(self, id_reporte):
        """Elimina un reporte"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reportes WHERE id_reporte = %s", (id_reporte,))
        conn.commit()
        cursor.close()
        conn.close()
        return True