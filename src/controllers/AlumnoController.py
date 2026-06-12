from models.AlumnoModel import AlumnoModel
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import date
import os

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

    def importar_excel(self, archivo, grado=None, grupo=None, especialidad=None, turno=None):
        if grado is None:
            grado = "2"
        if grupo is None:
            grupo = "D"
        if especialidad is None:
            especialidad = "Programación"
        if turno is None:
            turno = "Matutino"

        df = pd.read_excel(archivo, sheet_name=0, header=9)
        
        for _, row in df.iterrows():
            control = row.iloc[1]
            nombre_excel = row.iloc[2]
            
            if pd.isna(control):
                continue
                
            matricula = str(int(control)) if isinstance(control, float) else str(control)
            nombre_completo = str(nombre_excel).strip()
            nombre_completo = nombre_completo.replace("(Atencion)", "").strip()
            
            partes = nombre_completo.split()
            
            if len(partes) >= 3:
                apellido_paterno = partes[0]
                apellido_materno = partes[1]
                nombre = " ".join(partes[2:])
            elif len(partes) == 2:
                apellido_paterno = partes[0]
                apellido_materno = ""
                nombre = partes[1]
            else:
                apellido_paterno = ""
                apellido_materno = ""
                nombre = partes[0]

            semestre = str(grado)
            grupo_str = grupo
            especialidad_str = especialidad

            if not self.model.existe_matricula(matricula):
                self.model.crear_alumno(nombre, apellido_paterno, apellido_materno, matricula, grupo_str, semestre, especialidad_str)
            else:
                id_alumno = self.model.obtener_id_por_matricula(matricula)
                self.model.actualizar_alumno(id_alumno, nombre, apellido_paterno, apellido_materno, matricula, grupo_str, semestre, especialidad_str)

            id_alumno = self.model.obtener_id_por_matricula(matricula)

            asistencias_p1 = df.columns[4:34]
            for columna in asistencias_p1:
                valor = row[columna]
                if pd.isna(valor):
                    continue
                
                valor_str = str(valor).upper().strip()
                if valor is True or valor_str == "TRUE" or valor_str == "A" or valor_str == "ASISTIO":
                    estado = "Asistió"
                elif valor == 1 or valor == 1.0 or valor_str == "R" or valor_str == "RETARDO":
                    estado = "Retardo"
                else:
                    estado = "Falta"
                
                self.model.crear_asistencia(id_alumno, date.today(), estado)

            id_materia = 2
            
            p1 = None
            p2 = None
            p3 = None
            
            for col in df.columns:
                col_str = str(col).upper()
                if "CALF" in col_str or "CALIF" in col_str:
                    if "1" in col_str or "P1" in col_str:
                        p1 = row[col]
                    elif "2" in col_str or "P2" in col_str:
                        p2 = row[col]
                    elif "3" in col_str or "P3" in col_str:
                        p3 = row[col]
            
            if p1 is None:
                try:
                    p1 = row["Calf."]
                except:
                    pass
            if p2 is None:
                try:
                    p2 = row["Calf..1"]
                except:
                    pass
            if p3 is None:
                try:
                    p3 = row["Calf..2"]
                except:
                    pass
            
            if pd.notna(p1):
                try:
                    self.model.crear_calificacion(id_alumno, id_materia, 1, min(float(p1), 10))
                except:
                    pass
            if pd.notna(p2):
                try:
                    self.model.crear_calificacion(id_alumno, id_materia, 2, min(float(p2), 10))
                except:
                    pass
            if pd.notna(p3):
                try:
                    self.model.crear_calificacion(id_alumno, id_materia, 3, min(float(p3), 10))
                except:
                    pass
                    
        return True

    def generar_plantilla(self, grupo, semestre, especialidad):
        directorio_actual = os.path.dirname(__file__)
        directorio_src = os.path.dirname(directorio_actual)
        directorio_raiz = os.path.dirname(directorio_src)
        ruta_archivo = os.path.join(directorio_raiz, "Plantilla de grupo.xlsx")
        return "file:///" + ruta_archivo.replace("\\", "/")

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

    def corregir_nombres_existentes(self):
        alumnos = self.model.listar_alumnos()
        corregidos = 0
        
        for alumno in alumnos:
            nombre_actual = alumno.get('nombre', '')
            ap_paterno_actual = alumno.get('apellido_paterno', '')
            ap_materno_actual = alumno.get('apellido_materno', '')
            
            if len(nombre_actual) < 10 and len(ap_paterno_actual) < 10:
                nombre_completo = f"{nombre_actual} {ap_paterno_actual} {ap_materno_actual}"
                partes = nombre_completo.split()
                
                if len(partes) >= 3:
                    nuevo_apellido_paterno = partes[0]
                    nuevo_apellido_materno = partes[1]
                    nuevo_nombre = " ".join(partes[2:])
                    
                    self.model.actualizar_alumno(
                        alumno['id_alumno'],
                        nuevo_nombre,
                        nuevo_apellido_paterno,
                        nuevo_apellido_materno,
                        alumno['matricula'],
                        alumno['grupo'],
                        alumno['semestre'],
                        alumno['especialidad']
                    )
                    corregidos += 1
        
        return corregidos