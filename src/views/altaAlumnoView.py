import flet as ft

def AltaAlumnoView(page, alumno_controller, grupo_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    estilo_textfield = {
        "border_color": VINO_PRINCIPAL,
        "focused_border_color": VINO_OSCURO,
        "cursor_color": VINO_PRINCIPAL,
        "bgcolor": BLANCO,
        "border_radius": 12,
        "filled": True,
        "fill_color": GRIS_SUAVE,
    }

    estilo_dropdown = {
        "border_color": VINO_PRINCIPAL,
        "focused_border_color": VINO_OSCURO,
        "bgcolor": BLANCO,
        "border_radius": 12,
        "filled": True,
        "fill_color": GRIS_SUAVE,
    }

    dropdown_grupos = ft.Dropdown(
        label="Grupo (opcional, se puede editar después)",
        width=400,
        options=[],
        **estilo_dropdown,
    )

    def cargar_grupos_dropdown():
        grupos = grupo_controller.obtener_grupos()
        opciones = [ft.dropdown.Option(str(g["id_grupo"]), f"{g['grado']}° {g['grupo']} - {g['especialidad']}") for g in grupos]
        dropdown_grupos.options = opciones
        page.update()

    cargar_grupos_dropdown()

    txt_nombre = ft.TextField(label="Nombre *", width=350, **estilo_textfield)
    txt_apellido_paterno = ft.TextField(label="Apellido Paterno *", width=350, **estilo_textfield)
    txt_apellido_materno = ft.TextField(label="Apellido Materno", width=350, **estilo_textfield)
    txt_matricula = ft.TextField(label="Matrícula *", width=350, **estilo_textfield)
    txt_grupo = ft.TextField(label="Grupo (ej: D)", width=350, **estilo_textfield)
    txt_semestre = ft.TextField(label="Semestre (ej: 6)", width=350, **estilo_textfield)
    txt_especialidad = ft.TextField(label="Especialidad", width=350, **estilo_textfield)

    def limpiar_formulario(e=None):
        txt_nombre.value = ""
        txt_apellido_paterno.value = ""
        txt_apellido_materno.value = ""
        txt_matricula.value = ""
        txt_grupo.value = ""
        txt_semestre.value = ""
        txt_especialidad.value = ""
        page.update()

    def guardar_alumno(e):
        if not txt_nombre.value or not txt_apellido_paterno.value or not txt_matricula.value:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Nombre, apellido paterno y matrícula son obligatorios", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
            page.snack_bar.open = True
            page.update()
            return

        if dropdown_grupos.value:
            grupo_seleccionado = next((g for g in grupo_controller.obtener_grupos() if str(g["id_grupo"]) == dropdown_grupos.value), None)
            if grupo_seleccionado:
                txt_grupo.value = grupo_seleccionado["grupo"]
                txt_semestre.value = grupo_seleccionado["grado"]
                txt_especialidad.value = grupo_seleccionado["especialidad"]
                page.update()

        ok, msg = alumno_controller.guardar_alumno(
            txt_nombre.value,
            txt_apellido_paterno.value,
            txt_apellido_materno.value,
            txt_matricula.value,
            txt_grupo.value,
            txt_semestre.value,
            txt_especialidad.value
        )

        page.snack_bar = ft.SnackBar(ft.Text(msg, color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
        page.snack_bar.open = True
        if ok:
            limpiar_formulario()
        page.update()

    return ft.Column(
        [
            ft.Text("📝 Alta Manual de Alumnos", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            ft.Container(
                padding=30,
                bgcolor=BLANCO,
                border_radius=20,
                shadow=ft.BoxShadow(blur_radius=8, color="#D3D3D3"),
                content=ft.Column(
                    [
                        ft.Text("Ingrese los datos del alumno", size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([txt_nombre, txt_apellido_paterno], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        ft.Row([txt_apellido_materno, txt_matricula], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        ft.Row([txt_grupo, txt_semestre], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        txt_especialidad,
                        ft.Divider(height=10, color="transparent"),
                        ft.Text("Opcional: selecciona un grupo existente para precargar datos", size=12, color=VINO_CLARO),
                        dropdown_grupos,
                        ft.Row(
                            [
                                ft.ElevatedButton("💾 Guardar alumno", on_click=guardar_alumno, icon=ft.icons.SAVE, bgcolor=VINO_PRINCIPAL, color=BLANCO),
                                ft.OutlinedButton(
                                    "🗑️ Limpiar",
                                    on_click=limpiar_formulario,
                                    icon=ft.icons.CLEAR,
                                    style=ft.ButtonStyle(
                                        color=VINO_PRINCIPAL,
                                        side=ft.BorderSide(1, VINO_PRINCIPAL),
                                        shape=ft.RoundedRectangleBorder(radius=30),
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )