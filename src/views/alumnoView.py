import flet as ft

def AlumnoView(page, alumno_controller):

    info_alumno = ft.Column()

    alumnos = alumno_controller.obtener_alumnos()

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

            info_alumno.controls = [

                ft.Text(f'Nombre: {alumno["nombre"]}'),

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
                )

            ]

            page.update()

    dropdown_alumnos.on_change = mostrar_info

    return ft.View(

        route="/alumnos",

        controls=[

            ft.Column(

                [

                    ft.Text(
                        "Consulta de alumnos",
                        size=30,
                        weight=ft.FontWeight.BOLD
                    ),

                    dropdown_alumnos,

                    ft.Divider(),

                    info_alumno

                ],

                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            )

        ]
    )