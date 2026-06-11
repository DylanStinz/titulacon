from models.AlumnoModel import AlumnoModel
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import date

class AlumnoController:

    def __init__(self):
        self.model = AlumnoModel()

    def obtener_alumnos(self):
        return self.model.listar_alumnos()

    def obtener_calificaciones_alumno(self, id_alumno):
        return self.model.obtener_calificaciones_alumno(id_alumno)

    def guardar_alumno(self, nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad):
        if not nombre:
            return False, "El nombre es obligatorio"
        if not matricula:
            return False, "La matrícula es obligatoria"
        self.model.crear_alumno(nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad)
        return True, "Alumno registrado"

    def importar_excel(self, archivo):
        df = pd.read_excel(archivo, sheet_name=0, header=9)
        
        for _, row in df.iterrows():
            control = row.iloc[1]
            nombre_excel = row.iloc[2]

            if pd.isna(control):
                continue

            matricula = str(control)
            nombre_completo = str(nombre_excel)
            partes = nombre_completo.strip().split()

            apellido_paterno = partes[0] if len(partes) > 0 else ""
            apellido_materno = partes[1] if len(partes) > 1 else ""
            nombre = " ".join(partes[2:]) if len(partes) > 2 else ""

            semestre = "2"
            especialidad = "Programación"
            grupo = "D"

            if not self.model.existe_matricula(matricula):
                self.model.crear_alumno(nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad)
            else:
                id_alumno = self.model.obtener_id_por_matricula(matricula)
                self.model.actualizar_alumno(id_alumno, nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad)

            id_alumno = self.model.obtener_id_por_matricula(matricula)
            
            asistencias_p1 = df.columns[4:34]

            for columna in asistencias_p1:
                valor = row[columna]

                if pd.isna(valor):
                    continue

                if valor is True:
                    estado = "Asistió"
                elif valor == 1 or valor == 1.0:
                    estado = "Retardo"
                else:
                    estado = "Falta"

                self.model.crear_asistencia(id_alumno, date.today(), estado)

            id_materia = 2

            p1 = row["Calf."]
            p2 = row["Calf..1"]
            p3 = row["Calf..2"]

            if pd.notna(p1):
                self.model.crear_calificacion(id_alumno, id_materia, 1, min(float(p1), 10))
            if pd.notna(p2):
                self.model.crear_calificacion(id_alumno, id_materia, 2, min(float(p2), 10))
            if pd.notna(p3):
                self.model.crear_calificacion(id_alumno, id_materia, 3, min(float(p3), 10))

        return True

    def generar_plantilla(self, grupo, semestre, especialidad):
        wb = Workbook()
        ws = wb.active
        ws.title = "Calificaciones"
        encabezados = ["Matrícula", "Nombre", "Grupo", "Semestre", "Especialidad", "Parcial 1", "Parcial 2", "Parcial 3"]
        for col, encabezado in enumerate(encabezados, start=1):
            ws.cell(row=1, column=col, value=encabezado)
        archivo = f"Plantilla_{grupo}_{semestre}.xlsx"
        wb.save(archivo)
        return archivo

    def exportar_excel(self):
        alumnos = self.model.listar_alumnos()
        wb = Workbook()
        ws = wb.active
        ws.title = "Alumnos"
        encabezados = ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Matrícula", "Grupo", "Semestre", "Especialidad", "Estatus"]
        for col, encabezado in enumerate(encabezados, start=1):
            ws.cell(row=1, column=col, value=encabezado)
        for row_idx, alumno in enumerate(alumnos, start=2):
            ws.cell(row=row_idx, column=1, value=alumno.get("id_alumno", ""))
            ws.cell(row=row_idx, column=2, value=alumno.get("nombre", ""))
            ws.cell(row=row_idx, column=3, value=alumno.get("apellido_paterno", ""))
            ws.cell(row=row_idx, column=4, value=alumno.get("apellido_materno", ""))
            ws.cell(row=row_idx, column=5, value=alumno.get("matricula", ""))
            ws.cell(row=row_idx, column=6, value=alumno.get("grupo", ""))
            ws.cell(row=row_idx, column=7, value=alumno.get("semestre", ""))
            ws.cell(row=row_idx, column=8, value=alumno.get("especialidad", ""))
            ws.cell(row=row_idx, column=9, value=alumno.get("estatus", "Activo"))
        archivo = "Alumnos_exportados.xlsx"
        wb.save(archivo)
        return archivo

    def obtener_asistencias_alumno(self, id_alumno):
        return self.model.obtener_asistencias_alumno(id_alumno)
    
    def crear_asistencia(self, id_alumno, fecha, estado):
        if hasattr(fecha, 'date'):
            fecha = fecha.date()
        self.model.crear_asistencia(id_alumno, fecha, estado)
        return True, "Asistencia registrada correctamente"