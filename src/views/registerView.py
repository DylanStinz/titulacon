import flet as ft

def RegisterView(page, auth_controller):
    nombre = ft.TextField(label="Nombre", width=350)
    apellido = ft.TextField(label="Apellido", width=350)
    email = ft.TextField(label="Correo", width=350)
    password = ft.TextField(label="Contraseña", password=True, width=350)

    def register_click(e):
        if not nombre.value or not apellido.value or not email.value or not password.value:
            page.snack_bar = ft.SnackBar(ft.Text("Completa todos los campos"))
            page.snack_bar.open = True
            page.update()
            return

        ok, msg = auth_controller.registrar_usuario(
            nombre.value,
            apellido.value,
            email.value,
            password.value
        )

        if ok:
            page.snack_bar = ft.SnackBar(ft.Text("Usuario registrado correctamente"))
            page.snack_bar.open = True
            page.go("/")  
        else:
            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True

        page.update()

    return ft.View(
        route="/register",
        controls=[
            ft.Column(
                [
                    ft.AppBar(title=ft.Text("Registro")),
                    nombre,
                    apellido,
                    email,
                    password,
                    ft.ElevatedButton("Registrarse", on_click=register_click),
                    ft.TextButton("Volver", on_click=lambda _: page.go("/"))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
    )