from models.EstadisticasModel import EstadisticasModel
class EstadisticasController:

    def __init__(self):
        self.model = EstadisticasModel()

    def obtener_estadisticas(self):

        alumnos = self.model.total_alumnos()
        aprobados = self.model.total_aprobados()
        reprobados = self.model.total_reprobados()

        porcentaje = 0

        if alumnos > 0:
            porcentaje = round((aprobados / alumnos) * 100, 2)

        return {
            "alumnos": alumnos,
            "promedio": self.model.promedio_general(),
            "aprobados": aprobados,
            "reprobados": reprobados,
            "porcentaje": porcentaje
        }