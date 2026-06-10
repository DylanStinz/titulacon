from models.ReporteModel import ReporteModel

class ReporteController:

    def __init__(self):
        self.model = ReporteModel()
def obtener_reportes_por_alumno(self, id_alumno):
    """Obtiene reportes de un alumno específico"""
    return self.model.listar_reportes_por_alumno(id_alumno)

    def obtener_reporte(self, id_reporte):
        return self.model.obtener_reporte_por_id(id_reporte)

    def guardar_reporte(self, id_alumno, titulo, descripcion, tipo_reporte, estado):
        """Guarda un nuevo reporte"""
        if not titulo or not descripcion or not tipo_reporte or not estado:
            return False, "Todos los campos son obligatorios"
        
        if not id_alumno or id_alumno <= 0:
            return False, "Debe seleccionar un alumno válido"
        
        try:
            nuevo_id = self.model.crear_reporte(id_alumno, titulo, descripcion, tipo_reporte, estado)
            return True, f"Reporte creado exitosamente con ID: {nuevo_id}"
        except Exception as e:
            return False, f"Error al crear reporte: {str(e)}"

    def actualizar_reporte(self, id_reporte, titulo, descripcion, tipo_reporte, estado):
        if not titulo:
            return False, "El título es obligatorio"
        self.model.actualizar_reporte(id_reporte, titulo, descripcion, tipo_reporte, estado)
        return True, "Reporte actualizado correctamente"

    def eliminar_reporte(self, id_reporte):
        self.model.eliminar_reporte(id_reporte)
        return True, "Reporte eliminado correctamente"