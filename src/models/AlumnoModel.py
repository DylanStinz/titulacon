from .database import Database
from datetime import date

class AlumnoModel:

    def __init__(self):
        self.db = Database()

    def listar_alumnos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM alumnos"
        cursor.execute(query)
        alumnos = cursor.fetchall()
        cursor.close()
        conn.close()
        return alumnos

    def crear_alumno(self, nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO alumnos (nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        valores = (nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad)
        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def existe_matricula(self, matricula):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = "SELECT id_alumno FROM alumnos WHERE matricula = %s"
        cursor.execute(query, (matricula,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado is not None

    def obtener_id_por_matricula(self, matricula):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id_alumno FROM alumnos WHERE matricula = %s"
        cursor.execute(query, (matricula,))
        alumno = cursor.fetchone()
        cursor.close()
        conn.close()
        return alumno["id_alumno"] if alumno else None

    def crear_calificacion(self, id_alumno, id_materia, parcial, calificacion):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO calificaciones (id_alumno, id_materia, parcial, calificacion, fecha_registro)
        VALUES (%s,%s,%s,%s,CURDATE())
        """
        cursor.execute(query, (id_alumno, id_materia, parcial, calificacion))
        conn.commit()
        cursor.close()
        conn.close()

    def obtener_calificaciones_alumno(self, id_alumno):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT c.parcial, c.calificacion, m.nombre_materia
        FROM calificaciones c
        INNER JOIN materias m ON c.id_materia = m.id_materia
        WHERE c.id_alumno = %s
        ORDER BY c.parcial
        """
        cursor.execute(query, (id_alumno,))
        calificaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return calificaciones

    def obtener_alumno_por_id(self, id_alumno):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM alumnos WHERE id_alumno = %s"
        cursor.execute(query, (id_alumno,))
        alumno = cursor.fetchone()
        cursor.close()
        conn.close()
        return alumno

    def actualizar_alumno(self, id_alumno, nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        UPDATE alumnos 
        SET nombre = %s, apellido_paterno = %s, apellido_materno = %s, 
            matricula = %s, grupo = %s, semestre = %s, especialidad = %s
        WHERE id_alumno = %s
        """
        valores = (nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad, id_alumno)
        cursor.execute(query, valores)
        conn.commit()
        cursor.close()
        conn.close()

    def eliminar_alumno(self, id_alumno):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM calificaciones WHERE id_alumno = %s", (id_alumno,))
        cursor.execute("DELETE FROM asistencias WHERE id_alumno = %s", (id_alumno,))
        cursor.execute("DELETE FROM alumnos WHERE id_alumno = %s", (id_alumno,))
        conn.commit()
        cursor.close()
        conn.close()
    
    def crear_asistencia(self, id_alumno, fecha, estado):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO asistencias (id_alumno, fecha, estado)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (id_alumno, fecha, estado))
        conn.commit()
        cursor.close()
        conn.close()
    
    def obtener_asistencias_alumno(self, id_alumno):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT fecha, estado
        FROM asistencias
        WHERE id_alumno = %s
        ORDER BY fecha DESC
        """
        cursor.execute(query, (id_alumno,))
        asistencias = cursor.fetchall()
        cursor.close()
        conn.close()
        return asistencias