import flet as ft

def EstadisticasView(
    page,
    estadisticas_controller
):

    datos = (
        estadisticas_controller
        .obtener_estadisticas()
    )

    return ft.View(

        route="/estadisticas",

        appbar=ft.AppBar(
            title=ft.Text(
                "Estadísticas"
            )
        ),

        controls=[

            ft.Column(

                [

                    ft.Text(
                        "Panel de Estadísticas",
                        size=30,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Card(

                        content=ft.Container(

                            padding=20,

                            content=ft.Text(
                                f"👨‍🎓 Total alumnos: {datos['alumnos']}"
                            )
                        )
                    ),

                    ft.Card(

                        content=ft.Container(

                            padding=20,

                            content=ft.Text(
                                f"📈 Promedio general: {datos['promedio']}"
                            )
                        )
                    ),

                    ft.Card(

                        content=ft.Container(

                            padding=20,

                            content=ft.Text(
                                f"✅ Aprobados: {datos['aprobados']}"
                            )
                        )
                    ),

                    ft.Card(

                        content=ft.Container(

                            padding=20,

                            content=ft.Text(
                                f"❌ Reprobados: {datos['reprobados']}"
                            )
                        )
                    ),

                    ft.ElevatedButton(

                        "Volver",

                        icon=ft.icons.ARROW_BACK,

                        on_click=lambda _:
                        page.go("/dashboard")

                    )

                ],

                horizontal_alignment=
                ft.CrossAxisAlignment.CENTER

            )

        ]
    )