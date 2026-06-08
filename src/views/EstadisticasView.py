import flet as ft

def EstadisticasView(page, estadisticas_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    datos = estadisticas_controller.obtener_estadisticas()

    estilo_tarjeta = {
        "width": 280,
        "height": 140,
        "border_radius": 16,
        "bgcolor": BLANCO,
        "shadow": ft.BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color="#D3D3D3",
            offset=ft.Offset(0, 2),
        ),
        "border": ft.border.all(1, VINO_CLARO),
    }

    tarjeta_alumnos = ft.Container(
        **estilo_tarjeta,
        content=ft.Column(
            [
                ft.Icon(ft.icons.PEOPLE, color=VINO_PRINCIPAL, size=40),
                ft.Text(
                    "Total alumnos",
                    size=16,
                    color=VINO_OSCURO,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Text(
                    str(datos["alumnos"]),
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=VINO_PRINCIPAL,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
    )

    tarjeta_promedio = ft.Container(
        **estilo_tarjeta,
        content=ft.Column(
            [
                ft.Icon(ft.icons.ANALYTICS, color=VINO_PRINCIPAL, size=40),
                ft.Text(
                    "Promedio general",
                    size=16,
                    color=VINO_OSCURO,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Text(
                    str(datos["promedio"]),
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=VINO_PRINCIPAL,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
    )

    tarjeta_aprobados = ft.Container(
        **estilo_tarjeta,
        content=ft.Column(
            [
                ft.Icon(ft.icons.CHECK_CIRCLE, color=VINO_PRINCIPAL, size=40),
                ft.Text(
                    "Aprobados",
                    size=16,
                    color=VINO_OSCURO,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Text(
                    str(datos["aprobados"]),
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=VINO_PRINCIPAL,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
    )

    tarjeta_reprobados = ft.Container(
        **estilo_tarjeta,
        content=ft.Column(
            [
                ft.Icon(ft.icons.CANCEL, color=VINO_PRINCIPAL, size=40),
                ft.Text(
                    "Reprobados",
                    size=16,
                    color=VINO_OSCURO,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Text(
                    str(datos["reprobados"]),
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color=VINO_PRINCIPAL,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        ),
    )

    return ft.View(
        route="/estadisticas",
        scroll=ft.ScrollMode.AUTO,
        bgcolor=GRIS_SUAVE,
        appbar=ft.AppBar(
            title=ft.Text(
                "Estadísticas",
                color=BLANCO,
                size=22,
                weight=ft.FontWeight.BOLD,
            ),
            bgcolor=VINO_PRINCIPAL,
            center_title=True,
            elevation=4,
        ),
        controls=[
            ft.Container(
                padding=ft.padding.symmetric(horizontal=40, vertical=30),
                content=ft.Column(
                    [
                        # Encabezado decorativo
                        ft.Row(
                            [
                                ft.Icon(ft.icons.BAR_CHART, color=VINO_PRINCIPAL, size=40),
                                ft.Text(
                                    "Panel de Estadísticas",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=VINO_OSCURO,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=12,
                        ),
                        # Cuadrícula de tarjetas (responsive)
                        ft.ResponsiveRow(
                            [
                                ft.Column(
                                    col={"sm": 12, "md": 6, "lg": 3},
                                    controls=[tarjeta_alumnos],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    col={"sm": 12, "md": 6, "lg": 3},
                                    controls=[tarjeta_promedio],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    col={"sm": 12, "md": 6, "lg": 3},
                                    controls=[tarjeta_aprobados],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column(
                                    col={"sm": 12, "md": 6, "lg": 3},
                                    controls=[tarjeta_reprobados],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        # Botón volver
                        ft.ElevatedButton(
                            content=ft.Row(
                                [ft.Icon(ft.icons.ARROW_BACK), ft.Text("Volver al dashboard")],
                                spacing=8,
                            ),
                            on_click=lambda _: page.go("/dashboard"),
                            style=ft.ButtonStyle(
                                color=VINO_PRINCIPAL,
                                bgcolor=BLANCO,
                                side=ft.BorderSide(1.5, VINO_PRINCIPAL),
                                shape=ft.RoundedRectangleBorder(radius=30),
                            ),
                            width=250,
                        ),
                    ],
                    spacing=30,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ],
    )