import flet as ft

def LoginView(page, auth_controller):
    VINO = "#722F37"      
    VINO_OSCURO = "#4A1C22"
    BLANCO = "#FFFFFF"

    email_input = ft.TextField(
        label="Usuario",
        width=350,
        border_radius=10,
        bgcolor=BLANCO,
        border_color=VINO,
        focused_border_color=VINO_OSCURO,
        cursor_color=VINO,
    )

    pass_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
        border_radius=10,
        bgcolor=BLANCO,
        border_color=VINO,
        focused_border_color=VINO_OSCURO,
        cursor_color=VINO,
    )

    def login_click(e):
        if not email_input.value or not pass_input.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, complete todos los campos.", color=VINO_OSCURO),
                bgcolor=BLANCO,
            )
            page.snack_bar.open = True
            page.update()
            return

        user, msg = auth_controller.login(email_input.value, pass_input.value)

        if user:
            page.session.set("user", user)
            page.go("/menu")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text(msg, color=VINO_OSCURO),
                bgcolor=BLANCO,
            )
            page.snack_bar.open = True
            page.update()

    return ft.View(
        route="/",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=BLANCO,
        controls=[
            ft.Container(
                width=450,
                padding=30,
                border_radius=20,
                bgcolor=BLANCO,
                border=ft.border.all(1, VINO),
                content=ft.Column(
                    [
                        ft.Text(
                            "Iniciar Sesión",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=VINO,
                        ),
                        # Ícono de lápiz grande (similar a pluma)
                        ft.Icon(
                            ft.icons.CREATE,
                            size=80,
                            color=VINO,
                        ),
                        email_input,
                        pass_input,
                        ft.ElevatedButton(
                            "Ingresar",
                            width=350,
                            on_click=login_click,
                            style=ft.ButtonStyle(
                                color=BLANCO,
                                bgcolor=VINO,
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        ),
                        ft.TextButton(
                            "Crear cuenta",
                            on_click=lambda _: page.go("/register"),
                            style=ft.ButtonStyle(color=VINO),
                        ),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ],
    )
    