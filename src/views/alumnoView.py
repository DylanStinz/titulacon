import flet as ft

def AlumnoView(page, alumno_controller, grupo_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    info_alumno = ft.Column(spacing=12)
    dropdown_alumnos = ft.Dropdown(
        label="Seleccionar alumno",
        width=400,
        options=[],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=12,
        filled=True,
        fill_color=GRIS_SUAVE,
    )

    grupo_actual = None

    # ========== Asistencias ==========
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
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Selecciona fecha y estado", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
            page.snack_bar.open = True
            page.update()
            return

        fecha = fecha_asistencia.value
        if hasattr(fecha, 'date'):
            fecha = fecha.date()
        
        alumno_controller.crear_asistencia(alumno_id, fecha, estado_asistencia.value)

        page.snack_bar = ft.SnackBar(ft.Text("✅ Asistencia guardada", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
        page.snack_bar.open = True
        page.update()
        
        fecha_asistencia.value = None
        estado_asistencia.value = None
        mostrar_info(None)

    def abrir_fecha(e):
        fecha_asistencia.pick_date()
        page.update()
    # =================================

    def cargar_alumnos_por_grupo(grupo):
        nonlocal grupo_actual
        grupo_actual = grupo
        if grupo:
            todos = alumno_controller.obtener_alumnos()
            filtrados = [a for a in todos if str(a.get("semestre", "")) == str(grupo["grado"]) and a.get("grupo", "") == grupo["grupo"]]
        else:
            filtrados = []
        dropdown_alumnos.options = [
            ft.dropdown.Option(str(a["id_alumno"]), f'{a["nombre"]} {a["apellido_paterno"]}')
            for a in filtrados
        ]
        dropdown_alumnos.value = None
        info_alumno.controls = []
        page.update()

    def mostrar_info(e):
        alumno_id = dropdown_alumnos.value
        if not alumno_id or not grupo_actual:
            return
        todos = alumno_controller.obtener_alumnos()
        alumno = next((a for a in todos if str(a["id_alumno"]) == alumno_id and str(a.get("semestre", "")) == str(grupo_actual["grado"]) and a.get("grupo", "") == grupo_actual["grupo"]), None)
        if not alumno:
            return

        calificaciones = alumno_controller.obtener_calificaciones_alumno(alumno["id_alumno"])
        p1 = p2 = p3 = 0
        for c in calificaciones:
            if c["parcial"] == 1:
                p1 = min(float(c["calificacion"]), 10)
            elif c["parcial"] == 2:
                p2 = min(float(c["calificacion"]), 10)
            elif c["parcial"] == 3:
                p3 = min(float(c["calificacion"]), 10)

        validas = [x for x in [p1, p2, p3] if x > 0]
        promedio = round(sum(validas) / len(validas), 2) if validas else 0

        p1_mostrar = "Pendiente" if p1 == 0 else p1
        p2_mostrar = "Pendiente" if p2 == 0 else p2
        p3_mostrar = "Pendiente" if p3 == 0 else p3

        asistencias = alumno_controller.obtener_asistencias_alumno(alumno["id_alumno"])
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
                                ft.ElevatedButton("📅 Elegir fecha", on_click=abrir_fecha, icon=ft.icons.CALENDAR_MONTH),
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

    content = ft.Column(
        [
            ft.Text("📚 Gestión de Alumnos", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            ft.Row([dropdown_alumnos], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Text("📋 Información del Alumno", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            info_alumno,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )
    container = ft.Container(content=content)
    container.cargar_alumnos_por_grupo = cargar_alumnos_por_grupo
    return container


def GrupoView(page, grupo_controller, alumno_controller, on_grupo_seleccionado):
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

    # Botones de Excel
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def importar_excel_result(e):
        if e.files:
            archivo = e.files[0].path

            dlg_grado = ft.Dropdown(label="Grado", width=200, options=[ft.dropdown.Option(str(i)) for i in range(1, 7)])
            dlg_grupo = ft.TextField(label="Grupo", width=200)
            dlg_especialidad = ft.TextField(label="Especialidad", width=200)
            dlg_turno = ft.Dropdown(label="Turno", width=200, options=[ft.dropdown.Option("Matutino"), ft.dropdown.Option("Vespertino")], value="Matutino")

            def on_import_confirmar(e):
                grado_val = dlg_grado.value
                grupo_val = dlg_grupo.value
                especialidad_val = dlg_especialidad.value
                turno_val = dlg_turno.value
                if not (grado_val and grupo_val and especialidad_val and turno_val):
                    page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos del grupo", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
                    page.snack_bar.open = True
                    page.update()
                    return

                grupos_existentes = grupo_controller.obtener_grupos()
                existe = any(g for g in grupos_existentes if str(g["grado"]) == grado_val and g["grupo"] == grupo_val)
                if not existe:
                    ok, msg = grupo_controller.guardar_grupo(grado_val, grupo_val, especialidad_val, turno_val)
                    if not ok:
                        page.snack_bar = ft.SnackBar(ft.Text(f"Error al crear grupo: {msg}", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
                        page.snack_bar.open = True
                        page.update()
                        return

                try:
                    alumno_controller.importar_excel(archivo, grado_val, grupo_val, especialidad_val, turno_val)
                    page.snack_bar = ft.SnackBar(ft.Text("✅ Excel importado y grupo registrado", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
                    page.snack_bar.open = True
                    cargar_grupos()
                    dialog.open = False
                    page.update()
                except Exception as ex:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Error al importar: {ex}", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
                    page.snack_bar.open = True
                    page.update()

            dialog = ft.AlertDialog(
                title=ft.Text("Datos del grupo para la importación"),
                content=ft.Column([dlg_grado, dlg_grupo, dlg_especialidad, dlg_turno], spacing=10, tight=True),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
                    ft.ElevatedButton("Importar", on_click=on_import_confirmar),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

    file_picker.on_result = importar_excel_result

    def exportar_excel(e):
        archivo = alumno_controller.exportar_excel()
        page.snack_bar = ft.SnackBar(ft.Text("📎 Excel exportado", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
        page.snack_bar.open = True
        page.launch_url(archivo)
        page.update()

    def generar_plantilla(e):
        archivo = alumno_controller.generar_plantilla("D", 2, "Programación")
        page.snack_bar = ft.SnackBar(ft.Text("📄 Plantilla generada", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
        page.snack_bar.open = True
        page.launch_url(archivo)
        page.update()

    excel_buttons = ft.Row(
        [
            ft.ElevatedButton("📎 Exportar Excel", on_click=exportar_excel, icon=ft.icons.DOWNLOAD),
            ft.ElevatedButton("📄 Generar Plantilla", on_click=generar_plantilla, icon=ft.icons.TABLE_VIEW),
            ft.ElevatedButton("📤 Importar Excel", on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx"]), icon=ft.icons.UPLOAD),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    grupos_container = ft.Column(spacing=20)
    grupo_editando = {"id": None}

    def cargar_grupos():
        grupos_container.controls.clear()
        grupos = grupo_controller.obtener_grupos()
        grupos.sort(key=lambda g: (int(g["grado"]), g["grupo"]))

        grid = ft.GridView(
            expand=1,
            runs_count=4,
            max_extent=260,
            child_aspect_ratio=1.0,
            spacing=20,
            run_spacing=20,
        )
        for g in grupos:
            def seleccionar(e, grupo_data=g):
                if hasattr(e, 'control') and isinstance(e.control, ft.ElevatedButton):
                    return
                on_grupo_seleccionado(grupo_data)
                page.update()

            def editar(e, grupo_data=g):
                grupo_editando["id"] = grupo_data["id_grupo"]
                grado.value = str(grupo_data["grado"])
                grupo.value = grupo_data["grupo"]
                especialidad.value = grupo_data["especialidad"]
                turno.value = grupo_data["turno"]
                page.update()

            def eliminar(e, grupo_data=g):
                def confirmar_eliminar(e):
                    ok, msg = grupo_controller.eliminar_grupo(grupo_data["id_grupo"])
                    page.snack_bar = ft.SnackBar(ft.Text(msg, color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
                    page.snack_bar.open = True
                    dialog.open = False
                    cargar_grupos()
                    page.update()

                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("⚠️ Confirmar eliminación", color=VINO_OSCURO),
                    content=ft.Text(f"¿Eliminar el grupo {grupo_data['grado']}° {grupo_data['grupo']}?"),
                    actions=[
                        ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
                        ft.ElevatedButton("Eliminar", on_click=confirmar_eliminar, bgcolor="#F44336", color=BLANCO),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                page.dialog = dialog
                dialog.open = True
                page.update()

            tarjeta = ft.Card(
                elevation=3,
                color=BLANCO,
                shape=ft.RoundedRectangleBorder(radius=12),
                content=ft.Container(
                    width=240,
                    padding=12,
                    ink=True,
                    on_click=seleccionar,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.GROUP, color=VINO_PRINCIPAL, size=24),
                                    ft.Text(
                                        f"{g['grado']}° {g['grupo']}",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=VINO_OSCURO,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=8,
                            ),
                            ft.Text(
                                g['especialidad'],
                                size=12,
                                color=VINO_PRINCIPAL,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(f"Turno: {g['turno']}", size=11, color=VINO_CLARO),
                            ft.Divider(height=1, color=VINO_CLARO),
                            ft.Row(
                                [
                                    ft.ElevatedButton(
                                        "Editar",
                                        on_click=editar,
                                        icon=ft.icons.EDIT,
                                        style=ft.ButtonStyle(
                                            color=VINO_PRINCIPAL,
                                            bgcolor=BLANCO,
                                            side=ft.BorderSide(1, VINO_PRINCIPAL),
                                            shape=ft.RoundedRectangleBorder(radius=20),
                                        ),
                                        width=85,
                                        height=35,
                                    ),
                                    ft.ElevatedButton(
                                        "Eliminar",
                                        on_click=eliminar,
                                        icon=ft.icons.DELETE,
                                        style=ft.ButtonStyle(
                                            color=BLANCO,
                                            bgcolor="#F44336",
                                            shape=ft.RoundedRectangleBorder(radius=20),
                                        ),
                                        width=85,
                                        height=35,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            ),
                        ],
                        spacing=10,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
            )
            grid.controls.append(tarjeta)
        grupos_container.controls.append(grid)
        page.update()

    def guardar_grupo(e):
        if not (grado.value and grupo.value and especialidad.value and turno.value):
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Completa todos los campos", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
            page.snack_bar.open = True
            page.update()
            return
        if grupo_editando["id"]:
            ok, msg = grupo_controller.actualizar_grupo(grupo_editando["id"], grado.value, grupo.value, especialidad.value, turno.value)
            grupo_editando["id"] = None
        else:
            ok, msg = grupo_controller.guardar_grupo(grado.value, grupo.value, especialidad.value, turno.value)
        page.snack_bar = ft.SnackBar(ft.Text(msg, color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
        page.snack_bar.open = True
        if ok:
            grado.value = None
            grupo.value = ""
            especialidad.value = ""
            turno.value = None
            cargar_grupos()
        page.update()

    cargar_grupos()

    content = ft.Column(
        [
            ft.Text("👥 Gestión de Grupos", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            excel_buttons,
            ft.Divider(),
            ft.Text("Registrar nuevo grupo", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            ft.Row([grado, grupo], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            especialidad,
            turno,
            ft.ElevatedButton("💾 Guardar Grupo", on_click=guardar_grupo, icon=ft.icons.SAVE),
            ft.Divider(),
            ft.Text("📋 Grupos Registrados (haz clic en uno para seleccionarlo)", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            grupos_container,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    return ft.Container(content=content)
    