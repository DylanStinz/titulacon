from .database import Database

class AlumnoModel:

    def __init__(self):

        self.db = Database()

    def listar_alumnos(self):

        conn = self.db.get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM alumnos
        """

        cursor.execute(query)

        alumnos = cursor.fetchall()

        conn.close()

        return alumnos

    def crear_alumno(
        self,
        nombre,
        apellido_paterno,
        apellido_materno,
        matricula,
        grupo,
        semestre,
        especialidad
    ):

        conn = self.db.get_connection()

        cursor = conn.cursor()

        query = """
        INSERT INTO alumnos
        (
            nombre,
            apellido_paterno,
            apellido_materno,
            matricula,
            grupo,
            semestre,
            especialidad
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        valores = (

            nombre,
            apellido_paterno,
            apellido_materno,
            matricula,
            grupo,
            semestre,
            especialidad

        )

        cursor.execute(query, valores)

        conn.commit()

        conn.close()

        return True