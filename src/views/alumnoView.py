import flet as ft

def AlumnoView(page, alumno_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    info_alumno = ft.Column(spacing=12)
    fecha_picker = ft.DatePicker()
    page.overlay.append(fecha_picker)
    fecha_texto = ft.Text("📅 Sin fecha seleccionada")
    
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
    
    def abrir_fecha(e):
        fecha_picker.open = True
        page.update()

    def fecha_change(e):
        if fecha_picker.value:
            fecha_texto.value = f"📅 {fecha_picker.value}"
            page.update()

    fecha_picker.on_change = fecha_change
    fecha_asistencia = ft.DatePicker()
    page.overlay.append(fecha_asistencia)

    estado_asistencia = ft.Dropdown(
        label="Estado",
        width=200,
        options=[
            ft.dropdown.Option("Asistió"),
            ft.dropdown.Option("Falta"),
            ft.dropdown.Option("Retardo"),
        ],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
    )
    
    def guardar_asistencia(alumno_id):
        if not fecha_asistencia.value or not estado_asistencia.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Selecciona fecha y estado"))
            page.snack_bar.open = True
            page.update()
            return

        fecha = fecha_asistencia.value
        if hasattr(fecha, 'date'):
            fecha = fecha.date()
        
        alumno_controller.crear_asistencia(alumno_id, fecha, estado_asistencia.value)

        page.snack_bar = ft.SnackBar(ft.Text("✅ Asistencia guardada"))
        page.snack_bar.open = True
        page.update()
        
        fecha_asistencia.value = None
        estado_asistencia.value = None
        mostrar_info(None)

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
                    p1 = min(float(c["calificacion"]), 10)
                elif c["parcial"] == 2:
                    p2 = min(float(c["calificacion"]), 10)
                elif c["parcial"] == 3:
                    p3 = min(float(c["calificacion"]), 10)

            calificaciones_validas = []
            if p1 > 0:
                calificaciones_validas.append(p1)
            if p2 > 0:
                calificaciones_validas.append(p2)
            if p3 > 0:
                calificaciones_validas.append(p3)

            promedio = round(sum(calificaciones_validas) / len(calificaciones_validas), 2) if calificaciones_validas else 0

            p1_mostrar = "Pendiente" if p1 == 0 else p1
            p2_mostrar = "Pendiente" if p2 == 0 else p2
            p3_mostrar = "Pendiente" if p3 == 0 else p3

            asistencias = alumno_controller.obtener_asistencias_alumno(alumno["id_alumno"])
            if not asistencias:
                asistencias = []

            presentes = len([a for a in asistencias if a["estado"] == "Asistió"])
            faltas = len([a for a in asistencias if a["estado"] == "Falta"])
            retardos = len([a for a in asistencias if a["estado"] == "Retardo"])
            total_asistencias = len(asistencias)
            
            historial_textos = []
            for a in asistencias:
                fecha = a['fecha']
                if hasattr(fecha, 'strftime'):
                    fecha_str = fecha.strftime("%d/%m/%Y")
                else:
                    fecha_str = str(fecha)
                historial_textos.append(ft.Text(f"📆 {fecha_str} - {a['estado']}", size=14))
            
            if not historial_textos:
                historial_textos.append(ft.Text("No hay registros de asistencia", italic=True, color=VINO_CLARO))
            
            info_alumno.controls = [
                ft.Container(
                    padding=20,
                    bgcolor=BLANCO,
                    border_radius=16,
                    border=ft.border.all(1, VINO_CLARO),
                    content=ft.Column(
                        [
                            ft.Text(f"📛 Nombre: {alumno.get('nombre', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"📛 Apellido Paterno: {alumno.get('apellido_paterno', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"📛 Apellido Materno: {alumno.get('apellido_materno', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"🎓 Matrícula: {alumno.get('matricula', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"👥 Grupo: {alumno.get('grupo', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"📚 Semestre: {alumno.get('semestre', '')}", size=15, color=VINO_OSCURO),
                            ft.Text(f"💻 Especialidad: {alumno.get('especialidad', '')}", size=15, color=VINO_OSCURO),

                            ft.Divider(),

                            ft.Text("📖 CALIFICACIONES", size=16, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
                            ft.Text(f"Parcial 1: {p1_mostrar}", size=15, color=VINO_OSCURO),
                            ft.Text(f"Parcial 2: {p2_mostrar}", size=15, color=VINO_OSCURO),
                            ft.Text(f"Parcial 3: {p3_mostrar}", size=15, color=VINO_OSCURO),

                            ft.Divider(),

                            ft.Text(f"🎯 Promedio: {promedio}", size=18, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),

                            ft.Divider(),

                            ft.Text("📊 ASISTENCIAS", size=16, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),

                            ft.Text(f"✅ Asistió: {presentes}", size=14, color=VINO_OSCURO),
                            ft.Text(f"⚠️ Retardos: {retardos}", size=14, color=VINO_OSCURO),
                            ft.Text(f"❌ Faltas: {faltas}", size=14, color=VINO_OSCURO),
                            ft.Text(f"📅 Total registros: {total_asistencias}", size=14, color=VINO_PRINCIPAL),

                            ft.Divider(),

                            ft.Text("📌 REGISTRAR ASISTENCIA", weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),

                            ft.Row(
                                [
                                    ft.ElevatedButton("📅 Elegir fecha", on_click=lambda e: fecha_asistencia.pick_date(), icon=ft.icons.CALENDAR_MONTH),
                                    estado_asistencia,
                                    ft.ElevatedButton("💾 Guardar", on_click=lambda e: guardar_asistencia(alumno["id_alumno"]), icon=ft.icons.SAVE),
                                ],
                                spacing=10
                            ),

                            ft.Divider(),

                            ft.Text("📅 HISTORIAL DE ASISTENCIAS", weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
                        ] + historial_textos,
                        spacing=12,
                    ),
                )
            ]

            page.update()

    dropdown_alumnos.on_change = mostrar_info

    return ft.Column(
        [
            ft.Text("📚 Gestión de Alumnos", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            ft.Row([dropdown_alumnos], alignment=ft.MainAxisAlignment.CENTER),
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
        scroll=ft.ScrollMode.AUTO
    )


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
                        ft.Row(
                            [
                                ft.ElevatedButton("✏️ Editar", on_click=lambda e, g=g: editar_grupo(g), icon=ft.icons.EDIT),
                                ft.ElevatedButton("🗑️ Eliminar", on_click=lambda e, g=g: eliminar_grupo(g), icon=ft.icons.DELETE, color=ft.Colors.RED),
                            ],
                            spacing=10,
                        ),
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
    
    def eliminar_grupo(grupo_data):
        def confirmar_eliminar(e):
            ok, msg = grupo_controller.eliminar_grupo(grupo_data["id_grupo"])
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=BLANCO)
            page.snack_bar.open = True
            if ok:
                cargar_grupos()
                limpiar_formulario()
            page.update()
            dialog.open = False
            page.update()
        
        def cancelar_eliminar(e):
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de eliminar el grupo {grupo_data['grado']}° {grupo_data['grupo']}?"),
            actions=[
                ft.TextButton("Sí", on_click=confirmar_eliminar),
                ft.TextButton("No", on_click=cancelar_eliminar),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def limpiar_formulario():
        grupo_editando["id"] = None
        grado.value = None
        grupo.value = ""
        especialidad.value = ""
        turno.value = None
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
            limpiar_formulario()
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
            ft.Row(
                [
                    ft.ElevatedButton("💾 Guardar Grupo", on_click=guardar_grupo, icon=ft.icons.SAVE),
                    ft.ElevatedButton("🗑️ Limpiar", on_click=lambda e: limpiar_formulario(), icon=ft.icons.CLEAR),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Divider(),
            ft.Text("📋 Grupos Registrados", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            lista_grupos,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )