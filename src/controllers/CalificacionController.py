from models.CalificacionModel import CalificacionModel

class CalificacionController:

    def __init__(self):

        self.model = CalificacionModel()

    def obtener_calificaciones(
        self,
        id_alumno
    ):

        return self.model.obtener_calificaciones_alumno(
            id_alumno
        )