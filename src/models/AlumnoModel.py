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
    def existe_matricula(self, matricula):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        query = """
        SELECT id_alumno
        FROM alumnos
        WHERE matricula = %s
        """

        cursor.execute(query, (matricula,))

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        return resultado is not None
    
    def crear_calificacion(
            self,
            id_alumno,
            id_materia,
            parcial,
            calificacion
        ):

            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = """
            INSERT INTO calificaciones
            (
                id_alumno,
                id_materia,
                parcial,
                calificacion,
                fecha_registro
            )
            VALUES (%s,%s,%s,%s,CURDATE())
            """

            cursor.execute(
                query,
                (
                    id_alumno,
                    id_materia,
                    parcial,
                    calificacion
                )
            )

            conn.commit()

            cursor.close()
            conn.close()
    def obtener_id_por_matricula(self, matricula):

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id_alumno
        FROM alumnos
        WHERE matricula = %s
        """

        cursor.execute(query, (matricula,))

        alumno = cursor.fetchone()

        cursor.close()
        conn.close()

        return alumno["id_alumno"]