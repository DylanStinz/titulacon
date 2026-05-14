import flet as ft

def LoginView(page, auth_controller):

    email_input = ft.TextField(
        label="Usuario",
        width=350,
        border_radius=10
    )

    pass_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=10
    )

    def login_click(e):
        print("CLICK LOGIN")
        if not email_input.value or not pass_input.value:

            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, complete todos los campos.")
            )

            page.snack_bar.open = True
            page.update()

            return

        user, msg = auth_controller.login(

            email_input.value,
            pass_input.value

        )

        if user:

            page.session.user = user

            page.go("/dashboard")

        else:

            page.snack_bar = ft.SnackBar(
                ft.Text(msg)
            )

            page.snack_bar.open = True
            page.update()

    return ft.View(

        route="/",

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
                            "Iniciar Sesión",
                            size=30,
                            weight=ft.FontWeight.BOLD
                        ),

                        email_input,
                        pass_input,

                        ft.ElevatedButton(
                            "Ingresar",
                            width=350,
                            on_click=login_click
                        ),

                        ft.TextButton(
                            "Crear cuenta",
                            on_click=lambda _: page.go("/register")
                        )

                    ],

                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER

                )
            )
        ]
    )