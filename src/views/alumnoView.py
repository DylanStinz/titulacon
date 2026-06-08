import flet as ft

def AlumnoView(page, alumno_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    estilo_dropdown = {
        "border_color": VINO_PRINCIPAL,
        "focused_border_color": VINO_OSCURO,
        "bgcolor": BLANCO,
        "border_radius": 12,
        "filled": True,
        "fill_color": GRIS_SUAVE,
    }

    estilo_texto_info = {
        "size": 15,
        "color": VINO_OSCURO,
    }

    info_alumno = ft.Column(spacing=12)

    alumnos = alumno_controller.obtener_alumnos()

    def importar_excel_result(e):
        if e.files:
            archivo = e.files[0].path
            alumno_controller.importar_excel(archivo)
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Excel importado correctamente", color=VINO_OSCURO),
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            page.snack_bar.open = True
            page.update()

    def generar_plantilla(e):
        archivo = alumno_controller.generar_plantilla("D", 2, "Programación")
        page.snack_bar = ft.SnackBar(
            ft.Text("📄 Plantilla generada correctamente", color=VINO_OSCURO),
            bgcolor=BLANCO,
            behavior=ft.SnackBarBehavior.FLOATING,
            shape=ft.RoundedRectangleBorder(radius=8),
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
            ft.dropdown.Option(
                str(a["id_alumno"]),
                f'{a["nombre"]} {a["apellido_paterno"]}'
            )
            for a in alumnos
        ],
        **estilo_dropdown,
        icon=ft.icons.PERSON_SEARCH,
    )

    def mostrar_info(e):
        alumno_id = dropdown_alumnos.value
        alumno = next(
            (a for a in alumnos if str(a["id_alumno"]) == alumno_id),
            None
        )

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

            promedio = round((float(p1) + float(p2) + float(p3)) / 3, 2)

            info_alumno.controls = [
                ft.Container(
                    padding=20,
                    bgcolor=BLANCO,
                    border_radius=16,
                    border=ft.border.all(1, VINO_CLARO),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color="#D3D3D3",
                        offset=ft.Offset(0, 2),
                    ),
                    content=ft.Column(
                        [
                            # Datos personales
                            ft.Row(
                                [ft.Icon(ft.icons.PERSON, color=VINO_PRINCIPAL),
                                 ft.Text("Datos del alumno", size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO)],
                                spacing=10,
                            ),
                            ft.Divider(color=VINO_CLARO, thickness=1),
                            ft.Text(f"📛 Nombre: {alumno['nombre']}", **estilo_texto_info),
                            ft.Text(f"📛 Apellido: {alumno['apellido_paterno']}", **estilo_texto_info),
                            ft.Text(f"🎓 Matrícula: {alumno['matricula']}", **estilo_texto_info),
                            ft.Text(f"👥 Grupo: {alumno['grupo']}", **estilo_texto_info),
                            ft.Text(f"📚 Semestre: {alumno['semestre']}", **estilo_texto_info),
                            ft.Text(f"💼 Especialidad: {alumno['especialidad']}", **estilo_texto_info),
                            ft.Text(f"⚙️ Estatus: {alumno['estatus']}", **estilo_texto_info),
                            ft.Divider(color=VINO_CLARO, thickness=1),
                            # Calificaciones
                            ft.Row(
                                [ft.Icon(ft.icons.GRADE, color=VINO_PRINCIPAL),
                                 ft.Text("Calificaciones", size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO)],
                                spacing=10,
                            ),
                            ft.Divider(color=VINO_CLARO, thickness=1),
                            ft.Text(f"📖 Parcial 1: {p1}", **estilo_texto_info),
                            ft.Text(f"📖 Parcial 2: {p2}", **estilo_texto_info),
                            ft.Text(f"📖 Parcial 3: {p3}", **estilo_texto_info),
                            ft.Divider(color=VINO_CLARO, thickness=1),
                            ft.Row(
                                [ft.Icon(ft.icons.ANALYTICS, color=VINO_PRINCIPAL),
                                 ft.Text(f"Promedio: {promedio}", size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO)],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                )
            ]
            page.update()

    dropdown_alumnos.on_change = mostrar_info

    def exportar_excel(e):
        archivo = alumno_controller.exportar_excel()
        page.snack_bar = ft.SnackBar(
            ft.Text("📎 Excel exportado correctamente", color=VINO_OSCURO),
            bgcolor=BLANCO,
            behavior=ft.SnackBarBehavior.FLOATING,
            shape=ft.RoundedRectangleBorder(radius=8),
        )
        page.snack_bar.open = True
        page.launch_url(archivo)
        page.update()

    return ft.View(
        route="/alumnos",
        scroll=ft.ScrollMode.AUTO,
        bgcolor=GRIS_SUAVE,
        appbar=ft.AppBar(
            title=ft.Text("Consulta de Alumnos", color=BLANCO, size=22, weight=ft.FontWeight.BOLD),
            bgcolor=VINO_PRINCIPAL,
            center_title=True,
            elevation=4,
        ),
        controls=[
            ft.Container(
                padding=ft.padding.symmetric(horizontal=40, vertical=30),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.icons.SCHOOL, color=VINO_PRINCIPAL, size=40),
                                ft.Text(
                                    "Consulta de alumnos",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=VINO_OSCURO,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=12,
                        ),
                        # Dropdown de selección
                        ft.Container(
                            padding=20,
                            bgcolor=BLANCO,
                            border_radius=20,
                            shadow=ft.BoxShadow(
                                blur_radius=8,
                                color="#D3D3D3",
                                offset=ft.Offset(0, 2),
                            ),
                            content=ft.Column(
                                [
                                    dropdown_alumnos,
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                content=ft.Row([ft.Icon(ft.icons.DOWNLOAD), ft.Text("Exportar Excel")], spacing=8),
                                                on_click=exportar_excel,
                                                style=ft.ButtonStyle(
                                                    color=VINO_PRINCIPAL,
                                                    bgcolor=BLANCO,
                                                    side=ft.BorderSide(1.5, VINO_PRINCIPAL),
                                                    shape=ft.RoundedRectangleBorder(radius=30),
                                                ),
                                            ),
                                            ft.ElevatedButton(
                                                content=ft.Row([ft.Icon(ft.icons.TABLE_VIEW), ft.Text("Generar Plantilla")], spacing=8),
                                                on_click=generar_plantilla,
                                                style=ft.ButtonStyle(
                                                    color=VINO_PRINCIPAL,
                                                    bgcolor=BLANCO,
                                                    side=ft.BorderSide(1.5, VINO_PRINCIPAL),
                                                    shape=ft.RoundedRectangleBorder(radius=30),
                                                ),
                                            ),
                                            ft.ElevatedButton(
                                                content=ft.Row([ft.Icon(ft.icons.UPLOAD), ft.Text("Importar Excel")], spacing=8),
                                                on_click=lambda _: file_picker.pick_files(allowed_extensions=["xlsx"]),
                                                style=ft.ButtonStyle(
                                                    color=BLANCO,
                                                    bgcolor=VINO_PRINCIPAL,
                                                    shape=ft.RoundedRectangleBorder(radius=30),
                                                ),
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=15,
                                        wrap=True,
                                    ),
                                    ft.ElevatedButton(
                                        content=ft.Row([ft.Icon(ft.icons.ARROW_BACK), ft.Text("Volver")], spacing=8),
                                        on_click=lambda _: page.go("/dashboard"),
                                        style=ft.ButtonStyle(
                                            color=VINO_PRINCIPAL,
                                            bgcolor=BLANCO,
                                            side=ft.BorderSide(1.5, VINO_PRINCIPAL),
                                            shape=ft.RoundedRectangleBorder(radius=30),
                                        ),
                                        width=200,
                                    ),
                                ],
                                spacing=20,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),
                        ft.Divider(color=VINO_CLARO, height=2, thickness=1),
                        ft.Row(
                            [
                                ft.Icon(ft.icons.INFO, color=VINO_PRINCIPAL, size=28),
                                ft.Text(
                                    "Información del alumno",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=VINO_OSCURO,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        info_alumno,
                    ],
                    spacing=25,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ],
    )