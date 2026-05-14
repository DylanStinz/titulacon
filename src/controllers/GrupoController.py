from models.GrupoModel import GrupoModel

class GrupoController:

    def __init__(self):

        self.model = GrupoModel()

    def guardar_grupo(
        self,
        grado,
        grupo,
        especialidad,
        turno
    ):

        if not grado or not grupo:
            return False, "Completa los campos"

        self.model.crear_grupo(
            grado,
            grupo,
            especialidad,
            turno
        )

        return True, "Grupo registrado"

    def obtener_grupos(self):

        return self.model.listar_grupos()