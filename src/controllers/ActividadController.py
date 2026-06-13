class ActividadController:
    def __init__(self):
        self.actividades = []
        self.next_id = 1

    def obtener_actividades_por_grupo(self, id_grupo):
        return [a for a in self.actividades if a["id_grupo"] == id_grupo]

    def crear_actividad(self, id_grupo, titulo, descripcion, fecha_limite, asignatura):
        actividad = {
            "id_actividad": self.next_id,
            "id_grupo": id_grupo,
            "titulo": titulo,
            "descripcion": descripcion,
            "fecha_limite": fecha_limite,
            "asignatura": asignatura,
        }
        self.actividades.append(actividad)
        self.next_id += 1
        return True, "Actividad creada exitosamente"

    def actualizar_actividad(self, id_actividad, titulo, descripcion, fecha_limite, asignatura):
        for a in self.actividades:
            if a["id_actividad"] == id_actividad:
                a.update({
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "fecha_limite": fecha_limite,
                    "asignatura": asignatura,
                })
                return True, "Actividad actualizada"
        return False, "Actividad no encontrada"

    def eliminar_actividad(self, id_actividad):
        original_len = len(self.actividades)
        self.actividades = [a for a in self.actividades if a["id_actividad"] != id_actividad]
        if len(self.actividades) < original_len:
            return True, "Actividad eliminada"
        return False, "No se encontró la actividad"