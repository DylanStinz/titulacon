import flet as ft

def GrupoView(page, grupo_controller):

    grado = ft.Dropdown(
        label="Grado",
        width=145,
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
        width=145
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

    grupo_editando = {
        "id": None
    }

    def cargar_grupos():

        lista_grupos.controls.clear()

        grupos = grupo_controller.obtener_grupos()

        for g in grupos:

            alumnos = grupo_controller.obtener_alumnos_grupo(
                g["grupo"]
            )

            def editar_grupo(e, grupo_data=g):

                grupo_editando["id"] = grupo_data["id_grupo"]

                grado.value = str(grupo_data["grado"])
                grupo.value = grupo_data["grupo"]
                especialidad.value = grupo_data["especialidad"]
                turno.value = grupo_data["turno"]

                page.update()

            lista_grupos.controls.append(

                ft.Card(

                    content=ft.Container(

                        padding=15,

                        content=ft.Column(

                            [

                                ft.ListTile(

                                    leading=ft.Icon(
                                        ft.icons.GROUP
                                    ),

                                    title=ft.Text(
                                        f"{g['grado']}° {g['grupo']}"
                                    ),

                                    subtitle=ft.Text(
                                        f"{g['especialidad']} | {g['turno']}"
                                    )

                                ),

                                ft.Dropdown(

                                    label="Alumnos",

                                    width=250,

                                    options=[

                                        ft.dropdown.Option(
                                            f"{a['nombre']} {a['apellido_paterno']}"
                                        )

                                        for a in alumnos

                                    ]

                                ),

                                ft.ElevatedButton(

                                    "Editar",

                                    icon=ft.icons.EDIT,

                                    on_click=editar_grupo

                                )

                            ]

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

        if grupo_editando["id"]:

            ok, msg = grupo_controller.actualizar_grupo(

                grupo_editando["id"],
                grado.value,
                grupo.value,
                especialidad.value,
                turno.value

            )

            grupo_editando["id"] = None

        else:

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

            grado.value = None
            grupo.value = ""
            especialidad.value = ""
            turno.value = None

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

                        ft.Row(
                            [grado, grupo],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),

                        especialidad,

                        turno,

                        ft.ElevatedButton(
                            "Guardar Grupo",
                            icon=ft.icons.SAVE,
                            width=300,
                            on_click=guardar_grupo
                        ),

                        ft.ElevatedButton(
                            "Ir a alumnos",
                            icon=ft.icons.PEOPLE,
                            width=300,
                            on_click=lambda _: page.go("/alumnos")
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