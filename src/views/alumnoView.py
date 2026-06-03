import flet as ft

def AlumnoView(page, alumno_controller):

    info_alumno = ft.Column()

    alumnos = alumno_controller.obtener_alumnos()

    def importar_excel_result(e):

        if e.files:

            archivo = e.files[0].path

            alumno_controller.importar_excel(
                archivo
            )

            page.snack_bar = ft.SnackBar(
                ft.Text("Excel importado correctamente")
            )

            page.snack_bar.open = True

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

        ]

    )

    def mostrar_info(e):

        alumno_id = dropdown_alumnos.value

        alumno = next(

            (
                a for a in alumnos
                if str(a["id_alumno"]) == alumno_id
            ),

            None

        )

        if alumno:

            calificaciones = (
                alumno_controller.obtener_calificaciones_alumno(
                    alumno["id_alumno"]
                )
            )

            p1 = 0
            p2 = 0
            p3 = 0

            for c in calificaciones:

                if c["parcial"] == 1:

                    p1 = c["calificacion"]

                elif c["parcial"] == 2:

                    p2 = c["calificacion"]

                elif c["parcial"] == 3:

                    p3 = c["calificacion"]

            promedio = round(
                (
                    float(p1) +
                    float(p2) +
                    float(p3)
                ) / 3,
                2
            )

            info_alumno.controls = [

                ft.Text(
                    f'Nombre: {alumno["nombre"]}'
                ),

                ft.Text(
                    f'Apellido: {alumno["apellido_paterno"]}'
                ),

                ft.Text(
                    f'Matrícula: {alumno["matricula"]}'
                ),

                ft.Text(
                    f'Grupo: {alumno["grupo"]}'
                ),

                ft.Text(
                    f'Semestre: {alumno["semestre"]}'
                ),

                ft.Text(
                    f'Especialidad: {alumno["especialidad"]}'
                ),

                ft.Text(
                    f'Estatus: {alumno["estatus"]}'
                ),

                ft.Divider(),

                ft.Text(
                    "CALIFICACIONES",
                    size=20,
                    weight=ft.FontWeight.BOLD
                ),

                ft.Text(
                    f"Parcial 1: {p1}"
                ),

                ft.Text(
                    f"Parcial 2: {p2}"
                ),

                ft.Text(
                    f"Parcial 3: {p3}"
                ),

                ft.Divider(),

                ft.Text(
                    f"Promedio: {promedio}",
                    size=18,
                    weight=ft.FontWeight.BOLD
                )

            ]

            page.update()

    def exportar_excel(e):

        archivo = alumno_controller.exportar_excel()

        page.snack_bar = ft.SnackBar(
            ft.Text("Excel exportado correctamente")
        )

        page.snack_bar.open = True

        page.launch_url(archivo)

        page.update()

    dropdown_alumnos.on_change = mostrar_info

    return ft.View(

        route="/alumnos",

        appbar=ft.AppBar(
            title=ft.Text("Consulta de alumnos")
        ),

        controls=[

            ft.Column(

                [

                    ft.Text(
                        "Consulta de alumnos",
                        size=30,
                        weight=ft.FontWeight.BOLD
                    ),

                    dropdown_alumnos,

                    ft.ElevatedButton(

                        "Exportar Excel",

                        icon=ft.icons.DOWNLOAD,

                        on_click=exportar_excel

                    ),

                    ft.ElevatedButton(

                        "Importar Excel",

                        icon=ft.icons.UPLOAD,

                        on_click=lambda _: file_picker.pick_files(
                            allowed_extensions=["xlsx"]
                        )

                    ),

                    ft.ElevatedButton(

                        "Volver",

                        icon=ft.icons.ARROW_BACK,

                        on_click=lambda _: page.go("/dashboard")

                    ),

                    ft.Divider(),

                    info_alumno

                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            )

        ]

    )