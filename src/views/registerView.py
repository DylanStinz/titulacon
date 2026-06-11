import flet as ft
import re
def password_segura(password: str):
    if len(password) < 8:
        return False, "Debe tener mínimo 8 caracteres"

    if not re.search(r"[A-Z]", password):
        return False, "Debe contener al menos una mayúscula"

    if not re.search(r"[a-z]", password):
        return False, "Debe contener al menos una minúscula"

    if not re.search(r"[0-9]", password):
        return False, "Debe contener al menos un número"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-]", password):
        return False, "Debe contener al menos un carácter especial"

    return True, "OK"
def RegisterView(page, auth_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    estilo_textfield = {
        "width": 350,
        "border_radius": 12,
        "bgcolor": BLANCO,
        "filled": True,
        "fill_color": GRIS_SUAVE,
        "border_color": VINO_PRINCIPAL,
        "focused_border_color": VINO_OSCURO,
        "cursor_color": VINO_PRINCIPAL,
    }

    nombre = ft.TextField(label="Nombre", **estilo_textfield)
    apellido_paterno = ft.TextField(label="Apellido Paterno", **estilo_textfield)
    apellido_materno = ft.TextField(label="Apellido Materno", **estilo_textfield)
    correo = ft.TextField(
        label="Correo",
        keyboard_type=ft.KeyboardType.EMAIL,
        **estilo_textfield
    )
    usuario = ft.TextField(label="Usuario", **estilo_textfield)
    password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        **estilo_textfield
    )
    confirmar_password = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        **estilo_textfield
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
                ft.Text("⚠️ Completa todos los campos", color=VINO_OSCURO),
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            page.snack_bar.open = True
            page.update()
            return

        if "@" not in correo.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("✉️ Correo inválido", color=VINO_OSCURO),
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            page.snack_bar.open = True
            page.update()
            return

        ok_pass, msg_pass = password_segura(password.value)

        if not ok_pass:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"🔒 {msg_pass}", color=VINO_OSCURO),
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
            )
            page.snack_bar.open = True
            page.update()
            return

        if password.value != confirmar_password.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("❌ Las contraseñas no coinciden", color=VINO_OSCURO),
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
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
                ft.Text("✅ Usuario registrado correctamente", color=VINO_OSCURO),
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            page.snack_bar.open = True
            page.update()
            page.go("/")
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text(msg, color=VINO_OSCURO),
                bgcolor=BLANCO,
                behavior=ft.SnackBarBehavior.FLOATING,
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            page.snack_bar.open = True
            page.update()

    return ft.View(
        route="/register",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor=BLANCO,
        controls=[
            ft.Container(
                width=450,
                padding=30,
                border_radius=20,
                bgcolor=BLANCO,
                border=ft.border.all(1, VINO_PRINCIPAL),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color="#D3D3D3",
                    offset=ft.Offset(0, 2),
                ),
                content=ft.Column(
                    [
                        ft.Text(
                            "Registro de Docente",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=VINO_PRINCIPAL,
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
                            on_click=register_click,
                            style=ft.ButtonStyle(
                                color=BLANCO,
                                bgcolor=VINO_PRINCIPAL,
                                shape=ft.RoundedRectangleBorder(radius=30),
                                elevation=2,
                            ),
                        ),
                        ft.TextButton(
                            "Volver al inicio de sesión",
                            on_click=lambda _: page.go("/"),
                            style=ft.ButtonStyle(color=VINO_PRINCIPAL),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    tight=True,
                ),
            )
        ],
    )