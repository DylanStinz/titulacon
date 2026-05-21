from models.AlumnoModel import AlumnoModel

class AlumnoController:

    def __init__(self):

        self.model = AlumnoModel()

    def obtener_alumnos(self):

        return self.model.listar_alumnos()

    def guardar_alumno(
        self,
        nombre,
        apellido_paterno,
        apellido_materno,
        matricula,
        grupo,
        semestre,
        especialidad
    ):

        if not nombre:
            return False, "El nombre es obligatorio"

        if not matricula:
            return False, "La matrícula es obligatoria"

        self.model.crear_alumno(

            nombre,
            apellido_paterno,
            apellido_materno,
            matricula,
            grupo,
            semestre,
            especialidad

        )

        return True, "Alumno registrado"