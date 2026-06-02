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

    def importar_excel(self, archivo):

        df = pd.read_excel(
            archivo,
            sheet_name=0,
            header=9
        )

        print("COLUMNAS DEL EXCEL:")
        print(df.columns.tolist())

        print("PRIMERAS FILAS:")
        print(df.head())

        print("CALIFICACIONES:")
        print(df[["Calf.", "Calf..1", "Calf..2"]].head())

        for _, row in df.iterrows():

            control = row.iloc[1]
            nombre_excel = row.iloc[2]

            if pd.isna(control):
                continue

            matricula = str(control)

            nombre_completo = str(nombre_excel)

            partes = nombre_completo.split()

            nombre = partes[0]

            apellido_paterno = (
                partes[1]
                if len(partes) > 1 else ""
            )

            apellido_materno = (
                partes[2]
                if len(partes) > 2 else ""
            )

            semestre = "2"
            especialidad = "Programación"
            grupo = "D"

        if not self.model.existe_matricula(matricula):

            self.model.crear_alumno(
                nombre,
                apellido_paterno,
                apellido_materno,
                matricula,
                grupo,
                semestre,
                especialidad
            )

        id_alumno = self.model.obtener_id_por_matricula(
            matricula
        )

        id_materia = 1

        p1 = row["Calf."]
        p2 = row["Calf..1"]
        p3 = row["Calf..2"]

        if pd.notna(p1):

            self.model.crear_calificacion(
                id_alumno,
                id_materia,
                1,
                float(p1)
            )

        if pd.notna(p2):

            self.model.crear_calificacion(
                id_alumno,
                id_materia,
                2,
                float(p2)
            )

        if pd.notna(p3):

            self.model.crear_calificacion(
                id_alumno,
                id_materia,
                3,
                float(p3)
            )

        return True