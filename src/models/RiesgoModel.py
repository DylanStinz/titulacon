from .database import Database
from datetime import date

class RiesgoModel:

    def __init__(self):
        self.db = Database()

    def listar_riesgos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT r.*, a.nombre, a.apellido_paterno, a.apellido_materno, a.matricula
        FROM riesgo_academico r
        INNER JOIN alumnos a ON r.id_alumno = a.id_alumno
        ORDER BY r.fecha_registro DESC
        """
        cursor.execute(query)
        riesgos = cursor.fetchall()
        cursor.close()
        conn.close()
        return riesgos

    def listar_riesgos_por_alumno(self, id_alumno):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT * FROM riesgo_academico 
        WHERE id_alumno = %s 
        ORDER BY fecha_registro DESC
        """
        cursor.execute(query, (id_alumno,))
        riesgos = cursor.fetchall()
        cursor.close()
        conn.close()
        return riesgos

    def crear_riesgo(self, id_alumno, nivel_riesgo, motivo, seguimiento=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO riesgo_academico (id_alumno, nivel_riesgo, motivo, fecha_registro, seguimiento)
        VALUES (%s, %s, %s, CURDATE(), %s)
        """
        cursor.execute(query, (id_alumno, nivel_riesgo, motivo, seguimiento))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def actualizar_riesgo(self, id_riesgo, nivel_riesgo, motivo, seguimiento):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        UPDATE riesgo_academico 
        SET nivel_riesgo = %s, motivo = %s, seguimiento = %s
        WHERE id_riesgo = %s
        """
        cursor.execute(query, (nivel_riesgo, motivo, seguimiento, id_riesgo))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def eliminar_riesgo(self, id_riesgo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM riesgo_academico WHERE id_riesgo = %s", (id_riesgo,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def obtener_alumnos_riesgo_alto(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT DISTINCT r.id_alumno, a.nombre, a.apellido_paterno, a.apellido_materno, a.matricula, a.grupo
        FROM riesgo_academico r
        INNER JOIN alumnos a ON r.id_alumno = a.id_alumno
        WHERE r.nivel_riesgo = 'Alto'
        ORDER BY a.grupo, a.apellido_paterno
        """
        cursor.execute(query)
        alumnos = cursor.fetchall()
        cursor.close()
        conn.close()
        return alumnos