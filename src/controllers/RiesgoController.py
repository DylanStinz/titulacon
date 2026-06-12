from models.RiesgoModel import RiesgoModel

class RiesgoController:

    def __init__(self):
        self.model = RiesgoModel()

    def obtener_riesgos(self):
        return self.model.listar_riesgos()

    def obtener_riesgos_por_alumno(self, id_alumno):
        return self.model.listar_riesgos_por_alumno(id_alumno)

    def guardar_riesgo(self, id_alumno, nivel_riesgo, motivo, seguimiento=None):
        if not id_alumno:
            return False, "Debe seleccionar un alumno"
        if not nivel_riesgo:
            return False, "Debe seleccionar el nivel de riesgo"
        if not motivo:
            return False, "Debe especificar el motivo"
        
        self.model.crear_riesgo(id_alumno, nivel_riesgo, motivo, seguimiento)
        return True, "Riesgo académico registrado"

    def actualizar_riesgo(self, id_riesgo, nivel_riesgo, motivo, seguimiento):
        self.model.actualizar_riesgo(id_riesgo, nivel_riesgo, motivo, seguimiento)
        return True, "Riesgo académico actualizado"

    def eliminar_riesgo(self, id_riesgo):
        self.model.eliminar_riesgo(id_riesgo)
        return True, "Riesgo académico eliminado"

    def obtener_alumnos_riesgo_alto(self):
        return self.model.obtener_alumnos_riesgo_alto()