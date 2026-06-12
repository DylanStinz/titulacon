from models.ReporteModel import ReporteModel

class ReporteController:

    def __init__(self):
        self.model = ReporteModel()

    # Métodos existentes (para docentes)
    def obtener_reportes_por_docente(self, id_docente):
        return self.model.listar_reportes_por_docente(id_docente)

    def obtener_reporte(self, id_reporte):
        return self.model.obtener_reporte_por_id(id_reporte)

    def guardar_reporte(self, id_docente, tipo_reporte, descripcion):
        if not tipo_reporte or not descripcion:
            return False, "Todos los campos son obligatorios"
        try:
            nuevo_id = self.model.crear_reporte(id_docente, tipo_reporte, descripcion)
            return True, f"Reporte creado con ID: {nuevo_id}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def actualizar_reporte(self, id_reporte, tipo_reporte, descripcion):
        self.model.actualizar_reporte(id_reporte, tipo_reporte, descripcion)
        return True, "Reporte actualizado correctamente"

    def eliminar_reporte(self, id_reporte):
        self.model.eliminar_reporte(id_reporte)
        return True, "Reporte eliminado correctamente"

    # ========== NUEVOS MÉTODOS PARA REPORTES POR ALUMNO ==========
    def obtener_reportes_por_alumno(self, id_alumno):
        """Retorna lista de reportes de un alumno"""
        return self.model.listar_reportes_por_alumno(id_alumno)

    def guardar_reporte_alumno(self, id_alumno, id_docente, titulo, descripcion, tipo_reporte, estado):
        """Guarda un reporte asociado a un alumno y docente"""
        if not titulo or not descripcion:
            return False, "El título y la descripción son obligatorios"
        try:
            nuevo_id = self.model.crear_reporte_con_titulo(id_alumno, id_docente, titulo, descripcion, tipo_reporte, estado)
            return True, f"Reporte creado con ID: {nuevo_id}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def actualizar_reporte_alumno(self, id_reporte, titulo, descripcion, tipo_reporte, estado):
        """Actualiza un reporte existente"""
        self.model.actualizar_reporte_completo(id_reporte, titulo, descripcion, tipo_reporte, estado)
        return True, "Reporte actualizado correctamente"
        