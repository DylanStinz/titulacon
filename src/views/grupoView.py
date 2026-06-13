import flet as ft

def GrupoView(page, grupo_controller, alumno_controller, on_grupo_seleccionado):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_MUY_SUAVE = "#FAFAFA"

    estilo_dropdown = {
        "border_color": VINO_PRINCIPAL,
        "focused_border_color": VINO_OSCURO,
        "bgcolor": BLANCO,
        "border_radius": 12,
        "filled": True,
        "fill_color": GRIS_MUY_SUAVE,
    }

    estilo_textfield = {
        "border_color": VINO_PRINCIPAL,
        "focused_border_color": VINO_OSCURO,
        "cursor_color": VINO_PRINCIPAL,
        "bgcolor": BLANCO,
        "border_radius": 12,
        "filled": True,
        "fill_color": GRIS_MUY_SUAVE,
    }

    # ---------- DROPDOWN DE SELECCIÓN DE GRUPO ----------
    dropdown_grupos = ft.Dropdown(
        label="Seleccionar grupo",
        width=300,
        hint_text="Elige un grado y grupo",
        **estilo_dropdown,
    )

    def actualizar_dropdown_grupos():
        grupos = grupo_controller.obtener_grupos()
        opciones = []
        for g in grupos:
            opciones.append(
                ft.dropdown.Option(
                    key=str(g["id_grupo"]),
                    text=f"{g['grado']}° {g['grupo']} - {g['especialidad']} ({g['turno']})",
                    data=g
                )
            )
        dropdown_grupos.options = opciones
        page.update()

    def on_dropdown_change(e):
        if dropdown_grupos.value:
            grupo_data = next(
                (opt.data for opt in dropdown_grupos.options if opt.key == dropdown_grupos.value),
                None
            )
            if grupo_data and on_grupo_seleccionado:
                on_grupo_seleccionado(grupo_data)

    dropdown_grupos.on_change = on_dropdown_change

    # ---------- FORMULARIO DE REGISTRO / EDICIÓN ----------
    grado = ft.Dropdown(
        label="Grado",
        width=160,
        options=[ft.dropdown.Option(str(i)) for i in range(1, 7)],
        **estilo_dropdown,
    )

    grupo = ft.TextField(label="Grupo", width=160, **estilo_textfield)
    especialidad = ft.TextField(label="Especialidad", width=340, **estilo_textfield)
    turno = ft.Dropdown(
        label="Turno",
        width=340,
        options=[ft.dropdown.Option("Matutino"), ft.dropdown.Option("Vespertino")],
        **estilo_dropdown,
    )

    lista_grupos = ft.Column(spacing=20)
    grupo_editando = {"id": None}

    def cargar_grupos():
        lista_grupos.controls.clear()
        grupos = grupo_controller.obtener_grupos()

        for g in grupos:
            alumnos = grupo_controller.obtener_alumnos_grupo(g["grupo"])  # o usa id_grupo

            def editar_grupo(e, grupo_data=g):
                grupo_editando["id"] = grupo_data["id_grupo"]
                grado.value = str(grupo_data["grado"])
                grupo.value = grupo_data["grupo"]
                especialidad.value = grupo_data["especialidad"]
                turno.value = grupo_data["turno"]
                page.update()

            tarjeta = ft.Container(
                width=500,
                border_radius=16,
                bgcolor=BLANCO,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color="#D3D3D3",
                    offset=ft.Offset(0, 2),
                ),
                border=ft.border.all(1, VINO_CLARO),
                content=ft.Column(
                    [
                        ft.Container(
                            padding=ft.padding.only(top=16, left=16, right=16),
                            content=ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(
                                                f"{g['grado']}° {g['grupo']}",
                                                size=18,
                                                weight=ft.FontWeight.BOLD,
                                                color=VINO_OSCURO,
                                            ),
                                            ft.Text(
                                                f"{g['especialidad']} | {g['turno']}",
                                                size=13,
                                                color=VINO_PRINCIPAL,
                                            ),
                                        ],
                                        spacing=2,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=12,
                            ),
                        ),
                        ft.Divider(color=VINO_CLARO, height=1, thickness=1),
                        ft.Container(
                            padding=ft.padding.all(16),
                            content=ft.Column(
                                [
                                    ft.Dropdown(
                                        label="Alumnos del grupo",
                                        width=300,
                                        options=[
                                            ft.dropdown.Option(f"{a['nombre']} {a['apellido_paterno']}")
                                            for a in alumnos
                                        ],
                                        **estilo_dropdown,
                                    ),
                                    ft.ElevatedButton(
                                        "Editar grupo",
                                        on_click=editar_grupo,
                                        style=ft.ButtonStyle(
                                            color=VINO_PRINCIPAL,
                                            bgcolor=BLANCO,
                                            side=ft.BorderSide(1.5, VINO_PRINCIPAL),
                                            shape=ft.RoundedRectangleBorder(radius=30),
                                        ),
                                    ),
                                    ft.ElevatedButton(
                                        "Seleccionar este grupo",
                                        on_click=lambda e, g=g: on_grupo_seleccionado(g) if on_grupo_seleccionado else None,
                                        style=ft.ButtonStyle(
                                            color=BLANCO,
                                            bgcolor=VINO_PRINCIPAL,
                                            shape=ft.RoundedRectangleBorder(radius=30),
                                        ),
                                    ),
                                ],
                                spacing=12,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),
                    ],
                    spacing=0,
                ),
            )
            lista_grupos.controls.append(tarjeta)

        actualizar_dropdown_grupos()
        page.update()

    def guardar_grupo(e):
        if not (grado.value and grupo.value and especialidad.value and turno.value):
            page.snack_bar = ft.SnackBar(
                ft.Text("⚠️ Completa todos los campos", color=VINO_OSCURO),
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            page.snack_bar.open = True
            page.update()
            return

        if grupo_editando["id"]:
            ok, msg = grupo_controller.actualizar_grupo(
                grupo_editando["id"],
                grado.value,
                grupo.value,
                especialidad.value,
                turno.value,
            )
            grupo_editando["id"] = None
        else:
            ok, msg = grupo_controller.guardar_grupo(
                grado.value,
                grupo.value,
                especialidad.value,
                turno.value,
            )

        page.snack_bar = ft.SnackBar(
            ft.Text(msg, color=VINO_OSCURO),
            bgcolor=BLANCO,
            behavior=ft.SnackBarBehavior.FLOATING,
            shape=ft.RoundedRectangleBorder(radius=8),
        )
        page.snack_bar.open = True

        if ok:
            grado.value = None
            grupo.value = ""
            especialidad.value = ""
            turno.value = None
            cargar_grupos()

        page.update()

    # Cargar grupos al inicio
    cargar_grupos()

    # Retornar un control (Column) que se usará dentro del Tab
    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                padding=ft.padding.symmetric(horizontal=40, vertical=20),
                content=ft.Column(
                    [
                        # Selector de grupo (dropdown)
                        ft.Container(
                            padding=20,
                            bgcolor=BLANCO,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=8, color="#D3D3D3", offset=ft.Offset(0, 2)),
                            content=ft.Column(
                                [
                                    ft.Text("Seleccionar un grupo existente", size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
                                    dropdown_grupos,
                                ],
                                spacing=15,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),
                        ft.Divider(color=VINO_CLARO, height=2, thickness=1),
                        ft.Text(
                            "Registrar nuevo grupo",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=VINO_OSCURO,
                        ),
                        ft.Container(
                            padding=20,
                            bgcolor=BLANCO,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=8, color="#D3D3D3", offset=ft.Offset(0, 2)),
                            content=ft.Column(
                                [
                                    ft.Row([grado, grupo], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                                    especialidad,
                                    turno,
                                    ft.ElevatedButton(
                                        "Guardar grupo",
                                        width=280,
                                        on_click=guardar_grupo,
                                        style=ft.ButtonStyle(
                                            color=BLANCO,
                                            bgcolor=VINO_PRINCIPAL,
                                            shape=ft.RoundedRectangleBorder(radius=30),
                                            elevation=2,
                                        ),
                                    ),
                                ],
                                spacing=20,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),
                        ft.Divider(color=VINO_CLARO, height=2, thickness=1),
                        ft.Text(
                            "Grupos registrados",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=VINO_OSCURO,
                        ),
                        lista_grupos,
                    ],
                    spacing=25,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ],
    )