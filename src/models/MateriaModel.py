from .database import Database

class MateriaModel:

    def __init__(self):
        self.db = Database()

    def listar_materias(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM materias ORDER BY nombre_materia"
        cursor.execute(query)
        materias = cursor.fetchall()
        cursor.close()
        conn.close()
        return materias

    def crear_materia(self, nombre, semestre, especialidad):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO materias (nombre_materia, semestre, especialidad)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (nombre, semestre, especialidad))
        conn.commit()
        cursor.close()
        conn.close()

    def eliminar_materia(self, id_materia):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materias WHERE id_materia = %s", (id_materia,))
        conn.commit()
        cursor.close()
        conn.close()