import flet as ft

# ============================================================
# VISTA DE ALUMNOS
# ============================================================
def AlumnoView(page, alumno_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    info_alumno = ft.Column(spacing=12)
    
    def cargar_alumnos():
        return alumno_controller.obtener_alumnos()
    
    alumnos = cargar_alumnos()

    def importar_excel_result(e):
        if e.files:
            archivo = e.files[0].path
            alumno_controller.importar_excel(archivo)
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Excel importado correctamente", color=VINO_OSCURO),
                bgcolor=BLANCO,
            )
            page.snack_bar.open = True
            # Recargar dropdown
            nuevos_alumnos = cargar_alumnos()
            dropdown_alumnos.options = [
                ft.dropdown.Option(str(a["id_alumno"]), f'{a["nombre"]} {a["apellido_paterno"]}')
                for a in nuevos_alumnos
            ]
            page.update()

    def generar_plantilla(e):
        archivo = alumno_controller.generar_plantilla("D", 2, "Programación")
        page.snack_bar = ft.SnackBar(
            ft.Text("📄 Plantilla generada", color=VINO_OSCURO),
            bgcolor=BLANCO,
        )
        page.snack_bar.open = True
        page.launch_url(archivo)
        page.update()

    def exportar_excel(e):
        archivo = alumno_controller.exportar_excel()
        page.snack_bar = ft.SnackBar(
            ft.Text("📎 Excel exportado", color=VINO_OSCURO),
            bgcolor=BLANCO,
        )
        page.snack_bar.open = True
        page.launch_url(archivo)
        page.update()

    file_picker = ft.FilePicker()
    file_picker.on_result = importar_excel_result
    page.overlay.append(file_picker)

    dropdown_alumnos = ft.Dropdown(
        label="Seleccionar alumno",
        width=400,
        options=[
            ft.dropdown.Option(str(a["id_alumno"]), f'{a["nombre"]} {a["apellido_paterno"]}')
            for a in alumnos
        ],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=12,
        filled=True,
        fill_color=GRIS_SUAVE,
    )

    def mostrar_info(e):
        alumno_id = dropdown_alumnos.value
        if not alumno_id:
            return
        alumno = next((a for a in alumnos if str(a["id_alumno"]) == alumno_id), None)
        if alumno:
            calificaciones = alumno_controller.obtener_calificaciones_alumno(alumno["id_alumno"])
            p1 = p2 = p3 = 0
            for c in calificaciones:
                if c["parcial"] == 1:
                    p1 = c["calificacion"]
                elif c["parcial"] == 2:
                    p2 = c["calificacion"]
                elif c["parcial"] == 3:
                    p3 = c["calificacion"]
            promedio = round((float(p1) + float(p2) + float(p3)) / 3, 2) if calificaciones else 0
            info_alumno.controls = [
                ft.Container(
                    padding=20,
                    bgcolor=BLANCO,
                    border_radius=16,
                    border=ft.border.all(1, VINO_CLARO),
                    content=ft.Column(
                        [
                            ft.Text(f"📛 Nombre: {alumno.get('nombre', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"📛 Apellido: {alumno.get('apellido_paterno', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"🎓 Matrícula: {alumno.get('matricula', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"👥 Grupo: {alumno.get('grupo', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"📚 Semestre: {alumno.get('semestre', '')}", size=15, color=VINO_OSCURO),
                            ft.Divider(),
                            ft.Text(f"📖 Parcial 1: {p1}", size=15, color=VINO_OSCURO),
                            ft.Text(f"📖 Parcial 2: {p2}", size=15, color=VINO_OSCURO),
                            ft.Text(f"📖 Parcial 3: {p3}", size=15, color=VINO_OSCURO),
                            ft.Divider(),
                            ft.Text(f"🎯 Promedio: {promedio}", size=18, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
                        ],
                        spacing=10,
                    ),
                )
            ]
            page.update()

    dropdown_alumnos.on_change = mostrar_info

    # Retornar un Column con todo el contenido
    return ft.Column(
        [
            ft.Text("📚 Gestión de Alumnos", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            ft.Row(
                [
                    dropdown_alumnos,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.ElevatedButton("📎 Exportar Excel", on_click=exportar_excel, icon=ft.icons.DOWNLOAD),
                    ft.ElevatedButton("📄 Generar Plantilla", on_click=generar_plantilla, icon=ft.icons.TABLE_VIEW),
                    ft.ElevatedButton("📤 Importar Excel", on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx"]), icon=ft.icons.UPLOAD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Divider(),
            ft.Text("📋 Información del Alumno", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            info_alumno,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# ============================================================
# VISTA DE GRUPOS
# ============================================================
def GrupoView(page, grupo_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    grado = ft.Dropdown(
        label="Grado",
        width=150,
        options=[ft.dropdown.Option(str(i)) for i in range(1, 7)],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=10,
    )
    grupo = ft.TextField(label="Grupo", width=150, border_color=VINO_PRINCIPAL, focused_border_color=VINO_OSCURO)
    especialidad = ft.TextField(label="Especialidad", width=300, border_color=VINO_PRINCIPAL, focused_border_color=VINO_OSCURO)
    turno = ft.Dropdown(
        label="Turno",
        width=300,
        options=[ft.dropdown.Option("Matutino"), ft.dropdown.Option("Vespertino")],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=10,
    )
    
    lista_grupos = ft.Column(spacing=15)
    grupo_editando = {"id": None}
    
    def cargar_grupos():
        lista_grupos.controls.clear()
        grupos = grupo_controller.obtener_grupos()
        for g in grupos:
            tarjeta = ft.Container(
                width=500,
                padding=15,
                bgcolor=BLANCO,
                border_radius=12,
                border=ft.border.all(1, VINO_CLARO),
                content=ft.Column(
                    [
                        ft.Text(f"📌 {g['grado']}° {g['grupo']} - {g['especialidad']}", weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
                        ft.Text(f"🕒 Turno: {g['turno']}", size=13, color=VINO_CLARO),
                        ft.ElevatedButton("✏️ Editar", on_click=lambda e, g=g: editar_grupo(g), icon=ft.icons.EDIT),
                    ],
                    spacing=8,
                ),
            )
            lista_grupos.controls.append(tarjeta)
        page.update()
    
    def editar_grupo(grupo_data):
        grupo_editando["id"] = grupo_data["id_grupo"]
        grado.value = str(grupo_data["grado"])
        grupo.value = grupo_data["grupo"]
        especialidad.value = grupo_data["especialidad"]
        turno.value = grupo_data["turno"]
        page.update()
    
    def guardar_grupo(e):
        if not (grado.value and grupo.value and especialidad.value and turno.value):
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Completa todos los campos"), bgcolor=BLANCO)
            page.snack_bar.open = True
            page.update()
            return
        if grupo_editando["id"]:
            ok, msg = grupo_controller.actualizar_grupo(grupo_editando["id"], grado.value, grupo.value, especialidad.value, turno.value)
            grupo_editando["id"] = None
        else:
            ok, msg = grupo_controller.guardar_grupo(grado.value, grupo.value, especialidad.value, turno.value)
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=BLANCO)
        page.snack_bar.open = True
        if ok:
            grado.value = None
            grupo.value = ""
            especialidad.value = ""
            turno.value = None
            cargar_grupos()
        page.update()
    
    cargar_grupos()
    
    return ft.Column(
        [
            ft.Text("👥 Gestión de Grupos", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            ft.Row([grado, grupo], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            especialidad,
            turno,
            ft.ElevatedButton("💾 Guardar Grupo", on_click=guardar_grupo, icon=ft.icons.SAVE),
            ft.Divider(),
            ft.Text("📋 Grupos Registrados", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            lista_grupos,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )


# ============================================================
# VISTA DE CALIFICACIONES
# ============================================================
def CalificacionView(page, alumno_controller, calificacion_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"
    
    alumnos = alumno_controller.obtener_alumnos()
    info = ft.Column()
    
    dropdown = ft.Dropdown(
        label="Seleccionar Alumno",
        width=400,
        options=[
            ft.dropdown.Option(str(a["id_alumno"]), f'{a["nombre"]} {a["apellido_paterno"]}')
            for a in alumnos
        ],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=10,
    )
    
    def mostrar(e):
        if not dropdown.value:
            return
        calificaciones = calificacion_controller.obtener_calificaciones(dropdown.value)
        p1 = p2 = p3 = 0
        for c in calificaciones:
            if c["parcial"] == 1:
                p1 = c["calificacion"]
            elif c["parcial"] == 2:
                p2 = c["calificacion"]
            elif c["parcial"] == 3:
                p3 = c["calificacion"]
        promedio = round((float(p1) + float(p2) + float(p3)) / 3, 2) if calificaciones else 0
        info.controls = [
            ft.Container(
                padding=20,
                bgcolor=BLANCO,
                border_radius=16,
                border=ft.border.all(1, VINO_CLARO),
                content=ft.Column(
                    [
                        ft.Text(f"📖 Parcial 1: {p1}", size=18, color=VINO_OSCURO),
                        ft.Text(f"📖 Parcial 2: {p2}", size=18, color=VINO_OSCURO),
                        ft.Text(f"📖 Parcial 3: {p3}", size=18, color=VINO_OSCURO),
                        ft.Divider(),
                        ft.Text(f"🎯 Promedio Final: {promedio}", size=22, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ]
        page.update()
    
    dropdown.on_change = mostrar
    
    return ft.Column(
        [
            ft.Text("📖 Consulta de Calificaciones", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            dropdown,
            info,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )