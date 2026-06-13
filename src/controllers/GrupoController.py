from models.GrupoModel import GrupoModel

class GrupoController:

    def __init__(self):
        self.model = GrupoModel()

    def obtener_grupos(self):
        return self.model.listar_grupos()

    def guardar_grupo(self, grado, grupo, especialidad, materia, turno):
        if not grado or not grupo or not especialidad or not materia or not turno:
            return False, "Todos los campos son obligatorios"
        
        self.model.crear_grupo(grado, grupo, especialidad, materia, turno)
        return True, "Grupo guardado correctamente"

    def actualizar_grupo(self, id_grupo, grado, grupo, especialidad, materia, turno):
        if not grado or not grupo or not especialidad or not materia or not turno:
            return False, "Todos los campos son obligatorios"
        
        self.model.actualizar_grupo(id_grupo, grado, grupo, especialidad, materia, turno)
        return True, "Grupo actualizado correctamente"

    def eliminar_grupo(self, id_grupo):
        self.model.eliminar_grupo(id_grupo)
        return True, "Grupo eliminado correctamente"

    def obtener_alumnos_grupo(self, nombre_grupo):
        return self.model.obtener_alumnos_grupo(nombre_grupo)

    # Si aún quieres mantener la gestión de materias (tabla separada) para otros fines:
    def obtener_materias(self):
        from models.MateriaModel import MateriaModel
        materia_model = MateriaModel()
        return materia_model.listar_materias()

    def guardar_materia(self, nombre, semestre, especialidad):
        from models.MateriaModel import MateriaModel
        materia_model = MateriaModel()
        materia_model.crear_materia(nombre, semestre, especialidad)
        return True, "Materia guardada correctamente"

    def eliminar_materia(self, id_materia):
        from models.MateriaModel import MateriaModel
        materia_model = MateriaModel()
        materia_model.eliminar_materia(id_materia)
        return True, "Materia eliminada correctamente"