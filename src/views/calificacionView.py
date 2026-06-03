import flet as ft

def CalificacionView(
    page,
    alumno_controller,
    calificacion_controller
):

    alumnos = alumno_controller.obtener_alumnos()

    info = ft.Column()

    def mostrar(e):

        id_alumno = dropdown.value

        calificaciones = (
            calificacion_controller.obtener_calificaciones(
                id_alumno
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
            (float(p1) + float(p2) + float(p3)) / 3,
            2
        )

        info.controls = [

            ft.Text(
                f"Parcial 1: {p1}",
                size=20
            ),

            ft.Text(
                f"Parcial 2: {p2}",
                size=20
            ),

            ft.Text(
                f"Parcial 3: {p3}",
                size=20
            ),

            ft.Divider(),

            ft.Text(
                f"Promedio: {promedio}",
                size=24,
                weight=ft.FontWeight.BOLD
            )

        ]

        page.update()

    dropdown = ft.Dropdown(

        label="Alumno",

        width=400,

        options=[

            ft.dropdown.Option(
                str(a["id_alumno"]),
                f'{a["nombre"]} {a["apellido_paterno"]}'
            )

            for a in alumnos

        ],

        on_change=mostrar

    )

    return ft.View(

        route="/calificaciones",

        controls=[

            ft.Column(

                [

                    ft.Text(
                        "Consulta de Calificaciones",
                        size=30,
                        weight=ft.FontWeight.BOLD
                    ),

                    dropdown,

                    info,

                    ft.ElevatedButton(

                        "Volver",

                        on_click=lambda _:
                        page.go("/dashboard")

                    )

                ]

            )

        ]

    )