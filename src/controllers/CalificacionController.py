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
    def actualizar_calificacion(self, id_alumno, parcial, nueva_calificacion):
        return self.model.actualizar_calificacion(id_alumno, parcial, nueva_calificacion)