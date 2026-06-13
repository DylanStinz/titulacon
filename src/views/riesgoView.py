import flet as ft

def RiesgoView(page, riesgo_controller, alumno_controller, grupo_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    grupo_actual = None
    riesgos_container = ft.Column(spacing=15)

    def cargar_riesgos():
        riesgos = riesgo_controller.obtener_riesgos()
        
        riesgos_container.controls.clear()
        
        if not riesgos:
            riesgos_container.controls.append(
                ft.Container(
                    padding=40,
                    bgcolor=BLANCO,
                    border_radius=12,
                    content=ft.Text("📭 No hay registros de riesgo académico", size=14, color=VINO_CLARO),
                )
            )
        else:
            for r in riesgos:
                nivel_color = {
                    "Bajo": "#4CAF50",
                    "Medio": "#FF9800",
                    "Alto": "#F44336"
                }.get(r["nivel_riesgo"], VINO_PRINCIPAL)
                
                tarjeta = ft.Card(
                    elevation=3,
                    color=BLANCO,
                    shape=ft.RoundedRectangleBorder(radius=12),
                    content=ft.Container(
                        padding=15,
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.WARNING, color=nivel_color, size=24),
                                        ft.Text(
                                            f"{r['nombre']} {r['apellido_paterno']}",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=VINO_OSCURO,
                                        ),
                                        ft.Container(
                                            content=ft.Text(r["nivel_riesgo"], size=12, color=BLANCO),
                                            bgcolor=nivel_color,
                                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                            border_radius=12,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                ft.Text(f"Matrícula: {r['matricula']}", size=12, color=VINO_CLARO),
                                ft.Divider(height=1, color=VINO_CLARO),
                                ft.Text("📝 Motivo:", size=12, weight=ft.FontWeight.BOLD),
                                ft.Text(r["motivo"], size=12, color="#666"),
                                ft.Text("📌 Seguimiento:", size=12, weight=ft.FontWeight.BOLD) if r.get("seguimiento") else ft.Container(),
                                ft.Text(r.get("seguimiento", "Sin seguimiento"), size=12, color="#666") if r.get("seguimiento") else ft.Container(),
                                ft.Row(
                                    [
                                        ft.Text(f"📅 {r['fecha_registro']}", size=11, color=VINO_CLARO),
                                        ft.Row(
                                            [
                                                ft.IconButton(
                                                    icon=ft.icons.EDIT,
                                                    icon_size=18,
                                                    tooltip="Editar",
                                                    on_click=lambda e, rd=r: editar_riesgo(rd),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.icons.DELETE,
                                                    icon_size=18,
                                                    icon_color="#F44336",
                                                    tooltip="Eliminar",
                                                    on_click=lambda e, rd=r: eliminar_riesgo(rd),
                                                ),
                                            ],
                                            spacing=0,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ],
                            spacing=8,
                        ),
                    ),
                )
                riesgos_container.controls.append(tarjeta)
        
        page.update()

    def abrir_formulario_riesgo(riesgo=None):
        alumnos_list = alumno_controller.obtener_alumnos()
        
        if grupo_actual:
            alumnos_filtrados = [a for a in alumnos_list if str(a.get("grado", "")) == str(grupo_actual["grado"]) and a.get("grupo", "") == grupo_actual["grupo"]]
        else:
            alumnos_filtrados = alumnos_list
        
        alumno_dropdown = ft.Dropdown(
            label="Alumno",
            width=400,
            options=[
                ft.dropdown.Option(str(a["id_alumno"]), f"{a['nombre']} {a['apellido_paterno']} - {a['matricula']}")
                for a in alumnos_filtrados
            ],
            border_color=VINO_PRINCIPAL,
            focused_border_color=VINO_OSCURO,
            bgcolor=BLANCO,
            border_radius=12,
        )
        
        nivel_riesgo = ft.Dropdown(
            label="Nivel de Riesgo",
            width=400,
            options=[
                ft.dropdown.Option("Bajo", "🟢 Bajo"),
                ft.dropdown.Option("Medio", "🟡 Medio"),
                ft.dropdown.Option("Alto", "🔴 Alto"),
            ],
            border_color=VINO_PRINCIPAL,
            focused_border_color=VINO_OSCURO,
            bgcolor=BLANCO,
            border_radius=12,
        )
        
        motivo = ft.TextField(
            label="Motivo",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=400,
            border_color=VINO_PRINCIPAL,
        )
        
        seguimiento = ft.TextField(
            label="Seguimiento (opcional)",
            multiline=True,
            min_lines=2,
            max_lines=4,
            width=400,
            border_color=VINO_PRINCIPAL,
        )
        
        if riesgo:
            alumno_dropdown.value = str(riesgo["id_alumno"])
            nivel_riesgo.value = riesgo["nivel_riesgo"]
            motivo.value = riesgo["motivo"]
            seguimiento.value = riesgo.get("seguimiento", "")
            titulo = "✏️ Editar Riesgo Académico"
        else:
            titulo = "⚠️ Registrar Riesgo Académico"

        def guardar(e):
            if not alumno_dropdown.value:
                page.snack_bar = ft.SnackBar(ft.Text("⚠️ Selecciona un alumno"), bgcolor=GRIS_SUAVE)
                page.snack_bar.open = True
                page.update()
                return
            
            if not nivel_riesgo.value:
                page.snack_bar = ft.SnackBar(ft.Text("⚠️ Selecciona el nivel de riesgo"), bgcolor=GRIS_SUAVE)
                page.snack_bar.open = True
                page.update()
                return
            
            if not motivo.value:
                page.snack_bar = ft.SnackBar(ft.Text("⚠️ Escribe el motivo"), bgcolor=GRIS_SUAVE)
                page.snack_bar.open = True
                page.update()
                return
            
            if riesgo:
                ok, msg = riesgo_controller.actualizar_riesgo(
                    riesgo["id_riesgo"],
                    nivel_riesgo.value,
                    motivo.value,
                    seguimiento.value
                )
            else:
                ok, msg = riesgo_controller.guardar_riesgo(
                    int(alumno_dropdown.value),
                    nivel_riesgo.value,
                    motivo.value,
                    seguimiento.value
                )
            
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=GRIS_SUAVE)
            page.snack_bar.open = True
            dialog.open = False
            cargar_riesgos()
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text(titulo, color=VINO_PRINCIPAL),
            content=ft.Container(
                content=ft.Column(
                    [alumno_dropdown, nivel_riesgo, motivo, seguimiento],
                    spacing=15,
                    width=450,
                ),
                padding=10,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
                ft.ElevatedButton("Guardar", on_click=guardar, bgcolor=VINO_PRINCIPAL, color=BLANCO),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def editar_riesgo(riesgo):
        abrir_formulario_riesgo(riesgo)

    def eliminar_riesgo(riesgo):
        def confirmar(e):
            ok, msg = riesgo_controller.eliminar_riesgo(riesgo["id_riesgo"])
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=GRIS_SUAVE)
            page.snack_bar.open = True
            dialog.open = False
            cargar_riesgos()
            page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación", color=VINO_OSCURO),
            content=ft.Text(f"¿Eliminar el registro de riesgo para {riesgo['nombre']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False) or page.update()),
                ft.ElevatedButton("Eliminar", on_click=confirmar, bgcolor="#F44336", color=BLANCO),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def actualizar_por_grupo(grupo):
        nonlocal grupo_actual
        grupo_actual = grupo
        cargar_riesgos()

    content = ft.Column(
        [
            ft.Text("⚠️ Riesgo Académico", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "➕ Nuevo Registro",
                        on_click=lambda e: abrir_formulario_riesgo(),
                        icon=ft.icons.ADD_ALERT,
                        bgcolor=VINO_PRINCIPAL,
                        color=BLANCO,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(),
            ft.Text("📋 Registros de Riesgo Académico", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            riesgos_container,
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    
    container = ft.Container(content=content)
    container.actualizar_por_grupo = actualizar_por_grupo
    return container