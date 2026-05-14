import flet as ft

def GrupoView(page, grupo_controller):

    print("GrupoView cargado")

    grado = ft.Dropdown(
        label="Grado",
        width=300,
        options=[
            ft.dropdown.Option("1"),
            ft.dropdown.Option("2"),
            ft.dropdown.Option("3"),
            ft.dropdown.Option("4"),
            ft.dropdown.Option("5"),
            ft.dropdown.Option("6"),
        ]
    )

    grupo = ft.TextField(
        label="Grupo",
        width=300
    )

    especialidad = ft.TextField(
        label="Especialidad",
        width=300
    )

    turno = ft.Dropdown(
        label="Turno",
        width=300,
        options=[
            ft.dropdown.Option("Matutino"),
            ft.dropdown.Option("Vespertino")
        ]
    )

    lista_grupos = ft.Column()

    def cargar_grupos():

        lista_grupos.controls.clear()

        grupos = grupo_controller.obtener_grupos()

        for g in grupos:

            lista_grupos.controls.append(

                ft.Card(

                    content=ft.Container(

                        padding=15,

                        content=ft.ListTile(

                            leading=ft.Icon(ft.Icons.GROUP),

                            title=ft.Text(
                                f"{g['grado']}° {g['grupo']}"
                            ),

                            subtitle=ft.Text(
                                f"{g['especialidad']} | {g['turno']}"
                            )

                        )
                    )
                )
            )

        page.update()

    def guardar_grupo(e):

        if (
            not grado.value or
            not grupo.value or
            not especialidad.value or
            not turno.value
        ):

            page.snack_bar = ft.SnackBar(
                ft.Text("Completa todos los campos")
            )

            page.snack_bar.open = True
            page.update()

            return

        ok, msg = grupo_controller.guardar_grupo(

            grado.value,
            grupo.value,
            especialidad.value,
            turno.value

        )

        page.snack_bar = ft.SnackBar(
            ft.Text(msg)
        )

        page.snack_bar.open = True

        if ok:

            grupo.value = ""
            especialidad.value = ""

            cargar_grupos()

        page.update()

    cargar_grupos()

    return ft.View(

        route="/dashboard",

        scroll=ft.ScrollMode.AUTO,

        appbar=ft.AppBar(
            title=ft.Text("Gestión de Grupos")
        ),

        controls=[

            ft.Container(

                padding=30,

                content=ft.Column(

                    [

                        ft.Text(
                            "Registrar Grupo",
                            size=28,
                            weight=ft.FontWeight.BOLD
                        ),

                        grado,
                        grupo,
                        especialidad,
                        turno,

                        ft.ElevatedButton(
                            "Guardar Grupo",
                            icon=ft.Icons.SAVE,
                            width=300,
                            on_click=guardar_grupo
                        ),

                        ft.Divider(),

                        ft.Text(
                            "Grupos Registrados",
                            size=22,
                            weight=ft.FontWeight.BOLD
                        ),

                        lista_grupos

                    ],

                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER

                )
            )
        ]
    )