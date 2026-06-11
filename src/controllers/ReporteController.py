from models.ReporteModel import ReporteModel

class ReporteController:

    def __init__(self):
        self.model = ReporteModel()

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