from models.AlumnoModel import AlumnoModel
import pandas as pd

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

    def exportar_excel(self):

        alumnos = self.model.listar_alumnos()

        df = pd.DataFrame(alumnos)

        archivo = "alumnos.xlsx"

        df.to_excel(
            archivo,
            index=False
        )

        return archivo
    def importar_excel(self, archivo):

        df = pd.read_excel(archivo)

        for _, row in df.iterrows():

            self.model.crear_alumno(

                row["nombre"],
                row["apellido_paterno"],
                row["apellido_materno"],
                row["matricula"],
                row["grupo"],
                row["semestre"],
                row["especialidad"]

            )

        return True