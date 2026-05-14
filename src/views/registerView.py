import flet as ft

def RegisterView(page, auth_controller):

    nombre = ft.TextField(
        label="Nombre",
        width=350
    )

    apellido_paterno = ft.TextField(
        label="Apellido Paterno",
        width=350
    )

    apellido_materno = ft.TextField(
        label="Apellido Materno",
        width=350
    )

    correo = ft.TextField(
        label="Correo",
        width=350,
        keyboard_type=ft.KeyboardType.EMAIL
    )

    usuario = ft.TextField(
        label="Usuario",
        width=350
    )

    password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350
    )

    confirmar_password = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        width=350
    )

    def register_click(e):

        if (
            not nombre.value or
            not apellido_paterno.value or
            not apellido_materno.value or
            not correo.value or
            not usuario.value or
            not password.value or
            not confirmar_password.value
        ):

            page.snack_bar = ft.SnackBar(
                ft.Text("Completa todos los campos")
            )

            page.snack_bar.open = True
            page.update()
            return

        if "@" not in correo.value:

            page.snack_bar = ft.SnackBar(
                ft.Text("Correo inválido")
            )

            page.snack_bar.open = True
            page.update()
            return

        if len(password.value) < 6:

            page.snack_bar = ft.SnackBar(
                ft.Text("La contraseña debe tener mínimo 6 caracteres")
            )

            page.snack_bar.open = True
            page.update()
            return

        if password.value != confirmar_password.value:

            page.snack_bar = ft.SnackBar(
                ft.Text("Las contraseñas no coinciden")
            )

            page.snack_bar.open = True
            page.update()
            return

        ok, msg = auth_controller.registrar_usuario(

            nombre.value,
            apellido_paterno.value,
            apellido_materno.value,
            correo.value,
            usuario.value,
            password.value

        )

        if ok:

            page.snack_bar = ft.SnackBar(
                ft.Text("Usuario registrado correctamente")
            )

            page.snack_bar.open = True
            page.update()

            page.go("/")

        else:

            page.snack_bar = ft.SnackBar(
                ft.Text(msg)
            )

            page.snack_bar.open = True
            page.update()

    return ft.View(

        route="/register",

        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,

        controls=[

            ft.Container(

                width=450,
                padding=30,
                border_radius=20,

                content=ft.Column(

                    [

                        ft.Text(
                            "Registro de Docente",
                            size=30,
                            weight=ft.FontWeight.BOLD
                        ),

                        nombre,
                        apellido_paterno,
                        apellido_materno,
                        correo,
                        usuario,
                        password,
                        confirmar_password,

                        ft.ElevatedButton(
                            "Registrarse",
                            width=350,
                            on_click=register_click
                        ),

                        ft.TextButton(
                            "Volver al inicio de sesión",
                            on_click=lambda _: page.go("/")
                        )

                    ],

                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    tight=True

                )
            )
        ]
    )