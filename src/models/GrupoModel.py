from .database import Database

class GrupoModel:

    def __init__(self):
        self.db = Database()

    def crear_grupo(self, grado, grupo, especialidad, materia, turno):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO grupos (grado, grupo, especialidad, materia, turno)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (grado, grupo, especialidad, materia, turno)
        try:
            cursor.execute(query, valores)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()

    def listar_grupos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM grupos ORDER BY grado, grupo"
        cursor.execute(query)
        grupos = cursor.fetchall()
        cursor.close()
        conn.close()
        return grupos

    def obtener_alumnos_grupo(self, grupo):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM alumnos WHERE grupo = %s"
        cursor.execute(query, (grupo,))
        alumnos = cursor.fetchall()
        cursor.close()
        conn.close()
        return alumnos

    def actualizar_grupo(self, id_grupo, grado, grupo, especialidad, materia, turno):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = """
        UPDATE grupos 
        SET grado = %s, grupo = %s, especialidad = %s, materia = %s, turno = %s
        WHERE id_grupo = %s
        """
        valores = (grado, grupo, especialidad, materia, turno, id_grupo)
        try:
            cursor.execute(query, valores)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.close()

    def eliminar_grupo(self, id_grupo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM grupos WHERE id_grupo = %s"
        cursor.execute(query, (id_grupo,))
        conn.commit()
        cursor.close()
        conn.close()