from models.EstadisticasModel import EstadisticasModel

class EstadisticasController:

    def __init__(self):

        self.model = EstadisticasModel()

    def obtener_estadisticas(self):

        return {

            "alumnos":
                self.model.total_alumnos(),

            "promedio":
                self.model.promedio_general(),

            "aprobados":
                self.model.total_aprobados(),

            "reprobados":
                self.model.total_reprobados()

        }