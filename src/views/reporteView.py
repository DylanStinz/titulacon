import flet as ft

def ReporteView(page, alumno_controller, reporte_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"
    
    # Estado
    editando_id = None
    alumno_seleccionado_id = None
    
    # Contenedor de reportes
    lista_reportes = ft.Column(spacing=15)
    
    # Formulario para agregar/editar reporte
    form_container = ft.Column(visible=False, spacing=15)
    
    def cargar_alumnos():
        return alumno_controller.obtener_alumnos()
    
    def cargar_reportes():
        alumno_seleccionado_id = dropdown_alumnos.value  # este debe ser el id_alumno
        if alumno_seleccionado_id:
            reportes = reporte_controller.obtener_reportes_por_alumno(alumno_seleccionado_id)
        
        reportes = reporte_controller.obtener_reportes_por_alumno(alumno_seleccionado_id)
        
        if not reportes:
            lista_reportes.controls = [
                ft.Container(
                    padding=30,
                    bgcolor=BLANCO,
                    border_radius=16,
                    border=ft.border.all(1, VINO_CLARO, style=ft.BorderStyle.DASHED),
                    content=ft.Column(
                        [
                            ft.Icon(ft.icons.DESCRIPTION_OUTLINED, size=50, color=VINO_CLARO),
                            ft.Text("📭 No hay reportes para este alumno", size=16, color=VINO_CLARO),
                            ft.Text("Haz clic en 'Agregar Reporte' para crear uno", size=12, color=VINO_CLARO),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                )
            ]
            page.update()
            return
        
        lista_reportes.controls.clear()
        for r in reportes:
            # Colores según tipo
            tipo_colores = {
                "academico": ft.colors.BLUE_700,
                "conducta": ft.colors.ORANGE_700,
                "asistencia": ft.colors.GREEN_700,
                "otro": ft.colors.PURPLE_700
            }
            estado_colores = {
                "pendiente": ft.colors.ORANGE_700,
                "revisado": ft.colors.BLUE_700,
                "archivado": ft.colors.GREY_600
            }
            
            # Icono según tipo
            tipo_iconos = {
                "academico": ft.icons.SCHOOL,
                "conducta": ft.icons.WARNING,
                "asistencia": ft.icons.CALENDAR_TODAY,
                "otro": ft.icons.INFO
            }
            
            tarjeta = ft.Container(
                bgcolor=BLANCO,
                border_radius=12,
                border=ft.border.all(1, VINO_CLARO),
                padding=15,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(tipo_iconos.get(r["tipo_reporte"], ft.icons.DESCRIPTION), color=tipo_colores.get(r["tipo_reporte"], VINO_PRINCIPAL), size=28),
                                ft.Column(
                                    [
                                        ft.Text(r["titulo"], size=16, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
                                        ft.Row(
                                            [
                                                ft.Text(f"📅 {r['fecha_reporte']}", size=11, color=VINO_CLARO),
                                                ft.Container(width=5),
                                                ft.Container(
                                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                                    bgcolor=estado_colores.get(r["estado"], ft.colors.GREY_600),
                                                    border_radius=10,
                                                    content=ft.Text(r["estado"].upper(), size=9, color=BLANCO),
                                                ),
                                            ],
                                            spacing=5,
                                        ),
                                    ],
                                    spacing=3,
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.icons.EDIT_OUTLINED,
                                    icon_color=VINO_PRINCIPAL,
                                    tooltip="Editar reporte",
                                    on_click=lambda e, id_r=r["id_reporte"]: editar_reporte(id_r),
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE_OUTLINE,
                                    icon_color=ft.colors.RED_700,
                                    tooltip="Eliminar reporte",
                                    on_click=lambda e, id_r=r["id_reporte"]: eliminar_reporte(id_r),
                                ),
                            ],
                            spacing=10,
                        ),
                        ft.Text(r["descripcion"] if r["descripcion"] else "Sin descripción", size=13, color=VINO_OSCURO),
                    ],
                    spacing=10,
                ),
            )
            lista_reportes.controls.append(tarjeta)
        page.update()
    
    # Formulario campos
    titulo_input = ft.TextField(
        label="Título del reporte", 
        width=450, 
        border_color=VINO_PRINCIPAL, 
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        filled=True,
        fill_color=GRIS_SUAVE,
    )
    descripcion_input = ft.TextField(
        label="Descripción", 
        width=450, 
        multiline=True, 
        min_lines=3, 
        max_lines=5, 
        border_color=VINO_PRINCIPAL, 
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        filled=True,
        fill_color=GRIS_SUAVE,
    )
    tipo_input = ft.Dropdown(
        label="Tipo de reporte",
        width=200,
        options=[
            ft.dropdown.Option("academico", "📚 Académico"),
            ft.dropdown.Option("conducta", "⚠️ Conducta"),
            ft.dropdown.Option("asistencia", "📅 Asistencia"),
            ft.dropdown.Option("otro", "📌 Otro"),
        ],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        filled=True,
        fill_color=GRIS_SUAVE,
        value="academico",
    )
    estado_input = ft.Dropdown(
        label="Estado",
        width=200,
        options=[
            ft.dropdown.Option("pendiente", "⏳ Pendiente"),
            ft.dropdown.Option("revisado", "✓ Revisado"),
            ft.dropdown.Option("archivado", "📦 Archivado"),
        ],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        filled=True,
        fill_color=GRIS_SUAVE,
        value="pendiente",
    )
    
    def limpiar_formulario():
        titulo_input.value = ""
        descripcion_input.value = ""
        tipo_input.value = "academico"
        estado_input.value = "pendiente"
        page.update()
    
    def guardar_reporte(e):
        ok, msg = reporte_controller.guardar_reporte(
            id_alumno=alumno_seleccionado_id, 
            titulo=titulo_input.value,
            descripcion=descripcion_input.value,
            tipo_reporte=tipo_reporte_input.value,
            estado=estado_input.value
        )

        if editando_id:
            ok, msg = reporte_controller.actualizar_reporte(
                editando_id,
                titulo_input.value,
                descripcion_input.value,
                tipo_input.value,
                estado_input.value
            )
        else:
            ok, msg = reporte_controller.guardar_reporte(
                alumno_seleccionado_id,
                titulo_input.value,
                descripcion_input.value,
                tipo_input.value,
                estado_input.value
            )
        
        page.snack_bar = ft.SnackBar(
            ft.Text(msg, color=VINO_OSCURO), 
            bgcolor=BLANCO,
            behavior=ft.SnackBarBehavior.FLOATING,
        )
        page.snack_bar.open = True
        
        if ok:
            limpiar_formulario()
            cancelar_edicion(None)
            cargar_reportes()
        
        page.update()
    
    def editar_reporte(id_reporte):
        nonlocal editando_id
        editando_id = id_reporte
        reporte = reporte_controller.obtener_reporte(id_reporte)
        
        if reporte:
            titulo_input.value = reporte["titulo"]
            descripcion_input.value = reporte["descripcion"]
            tipo_input.value = reporte["tipo_reporte"]
            estado_input.value = reporte["estado"]
            
            form_container.visible = True
            btn_agregar.visible = False
            btn_cancelar_form.visible = True
            page.update()
    
    def eliminar_reporte(id_reporte):
        def confirmar(e):
            ok, msg = reporte_controller.eliminar_reporte(id_reporte)
            page.snack_bar = ft.SnackBar(
                ft.Text(msg, color=VINO_OSCURO), 
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
            )
            page.snack_bar.open = True
            dialog.open = False
            cargar_reportes()
            page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("⚠️ Confirmar eliminación", color=VINO_OSCURO),
            content=ft.Text("¿Eliminar este reporte? Esta acción no se puede deshacer."),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
                ft.ElevatedButton("Eliminar", on_click=confirmar, bgcolor="#F44336", color=BLANCO),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def mostrar_formulario(e):
        nonlocal editando_id
        editando_id = None
        limpiar_formulario()
        form_container.visible = True
        btn_agregar.visible = False
        btn_cancelar_form.visible = True
        page.update()
    
    def cancelar_edicion(e):
        nonlocal editando_id
        editando_id = None
        limpiar_formulario()
        form_container.visible = False
        btn_agregar.visible = True
        btn_cancelar_form.visible = False
        page.update()
    
    # Dropdown de alumnos
    alumnos = cargar_alumnos()
    dropdown_alumnos = ft.Dropdown(
        label="Seleccionar alumno",
        width=400,
        options=[
            ft.dropdown.Option(str(a["id_alumno"]), f'{a["nombre"]} {a["apellido_paterno"]} - {a["matricula"]}')
            for a in alumnos
        ],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=12,
        filled=True,
        fill_color=GRIS_SUAVE,
    )
    
    def on_alumno_change(e):
        nonlocal alumno_seleccionado_id, editando_id
        if dropdown_alumnos.value:
            alumno_seleccionado_id = int(dropdown_alumnos.value)
            cargar_reportes()
            cancelar_edicion(None)
        else:
            alumno_seleccionado_id = None
            lista_reportes.controls = [ft.Text("👈 Selecciona un alumno para ver sus reportes", color=VINO_CLARO, size=16)]
            page.update()
    
    dropdown_alumnos.on_change = on_alumno_change
    
    # Botones
    btn_agregar = ft.ElevatedButton(
        "➕ Agregar Reporte",
        on_click=mostrar_formulario,
        icon=ft.icons.ADD,
        style=ft.ButtonStyle(color=BLANCO, bgcolor=VINO_PRINCIPAL, shape=ft.RoundedRectangleBorder(radius=30)),
    )
    
    btn_cancelar_form = ft.ElevatedButton(
        "❌ Cancelar",
        on_click=cancelar_edicion,
        visible=False,
        icon=ft.icons.CLOSE,
        style=ft.ButtonStyle(color=BLANCO, bgcolor=ft.colors.GREY_600, shape=ft.RoundedRectangleBorder(radius=30)),
    )
    
    btn_guardar = ft.ElevatedButton(
        "💾 Guardar Reporte",
        on_click=guardar_reporte,
        icon=ft.icons.SAVE,
        style=ft.ButtonStyle(color=BLANCO, bgcolor=ft.colors.GREEN_700, shape=ft.RoundedRectangleBorder(radius=30)),
    )
    
    # Formulario
    form_container.controls = [
        ft.Text("📝 Nuevo Reporte", size=20, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
        titulo_input,
        descripcion_input,
        ft.Row([tipo_input, estado_input], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ft.Row([btn_guardar, btn_cancelar_form], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
    ]
    
    return ft.Column(
        [
            ft.Text("📋 Gestión de Reportes", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            ft.Text("Selecciona un alumno para gestionar sus reportes", size=14, color=VINO_CLARO),
            dropdown_alumnos,
            ft.Container(height=10),
            btn_agregar,
            form_container,
            ft.Divider(),
            ft.Text("📋 Lista de Reportes", size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            ft.Container(
                content=lista_reportes,
                height=350,
                width=650,
            ),
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )