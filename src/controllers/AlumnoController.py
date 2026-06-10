from models.AlumnoModel import AlumnoModel
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

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
            partes = nombre_completo.split()
            nombre = partes[0]
            apellido_paterno = partes[1] if len(partes) > 1 else ""
            apellido_materno = partes[2] if len(partes) > 2 else ""
            semestre = "2"
            especialidad = "Programación"
            grupo = "D"
            if not self.model.existe_matricula(matricula):
                self.model.crear_alumno(nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad)
            id_alumno = self.model.obtener_id_por_matricula(matricula)
            id_materia = 2
            p1 = row["Calf."]
            p2 = row["Calf..1"]
            p3 = row["Calf..2"]
            if pd.notna(p1):
                self.model.crear_calificacion(id_alumno, id_materia, 1, float(p1))
            if pd.notna(p2):
                self.model.crear_calificacion(id_alumno, id_materia, 2, float(p2))
            if pd.notna(p3):
                self.model.crear_calificacion(id_alumno, id_materia, 3, float(p3))
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
            ws.cell(row=row_idx, column=9, value=alumno.get("estatus", ""))
        archivo = "Alumnos_exportados.xlsx"
        wb.save(archivo)
        return archivo

    # ========== MÉTODOS NUEVOS PARA REPORTES ==========

    def actualizar_alumno(self, id_alumno, nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad):
        """Actualiza los datos de un alumno existente"""
        if not nombre or not matricula:
            return False, "El nombre y matrícula son obligatorios"
        self.model.actualizar_alumno(id_alumno, nombre, apellido_paterno, apellido_materno, matricula, grupo, semestre, especialidad)
        return True, "Alumno actualizado correctamente"

    def eliminar_alumno(self, id_alumno):
        """Elimina un alumno por su ID"""
        self.model.eliminar_alumno(id_alumno)
        return True, "Alumno eliminado correctamente"

    def generar_reporte_alumno(self, id_alumno):
        """Genera un reporte Excel del alumno"""
        alumno = self.model.obtener_alumno_por_id(id_alumno)
        if not alumno:
            return None
        
        calificaciones = self.model.obtener_calificaciones_alumno(id_alumno)
        
        wb = Workbook()
        ws = wb.active
        ws.title = f"Reporte_{alumno['nombre']}"
        
        # Título
        ws.merge_cells('A1:D1')
        ws['A1'] = f"REPORTE ACADÉMICO - {alumno['nombre']} {alumno['apellido_paterno']}"
        ws['A1'].font = Font(bold=True, size=14)
        ws['A1'].alignment = Alignment(horizontal='center')
        
        # Datos del alumno
        ws['A3'] = "DATOS DEL ALUMNO"
        ws['A3'].font = Font(bold=True, size=12)
        ws['A4'] = "Nombre:"
        ws['B4'] = alumno['nombre']
        ws['A5'] = "Apellido Paterno:"
        ws['B5'] = alumno['apellido_paterno']
        ws['A6'] = "Apellido Materno:"
        ws['B6'] = alumno['apellido_materno']
        ws['A7'] = "Matrícula:"
        ws['B7'] = alumno['matricula']
        ws['A8'] = "Grupo:"
        ws['B8'] = alumno['grupo']
        ws['A9'] = "Semestre:"
        ws['B9'] = alumno['semestre']
        ws['A10'] = "Especialidad:"
        ws['B10'] = alumno['especialidad']
        
        # Calificaciones
        ws['A12'] = "CALIFICACIONES"
        ws['A12'].font = Font(bold=True, size=12)
        ws['A13'] = "Parcial"
        ws['B13'] = "Calificación"
        ws['A13'].font = Font(bold=True)
        ws['B13'].font = Font(bold=True)
        
        row = 14
        p1 = p2 = p3 = 0
        for c in calificaciones:
            ws[f'A{row}'] = c["parcial"]
            ws[f'B{row}'] = c["calificacion"]
            if c["parcial"] == 1:
                p1 = c["calificacion"]
            elif c["parcial"] == 2:
                p2 = c["calificacion"]
            elif c["parcial"] == 3:
                p3 = c["calificacion"]
            row += 1
        
        promedio = round((float(p1) + float(p2) + float(p3)) / 3, 2) if calificaciones else 0
        
        ws[f'A{row+1}'] = "Promedio Final:"
        ws[f'B{row+1}'] = promedio
        ws[f'A{row+1}'].font = Font(bold=True)
        ws[f'B{row+1}'].font = Font(bold=True)
        
        # Ajustar anchos
        for col in ['A', 'B', 'C', 'D']:
            ws.column_dimensions[col].width = 20
        
        archivo = f"Reporte_{alumno['matricula']}_{alumno['nombre']}.xlsx"
        wb.save(archivo)
        return archivo