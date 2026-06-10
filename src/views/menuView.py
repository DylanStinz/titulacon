import flet as ft
from views.alumnoView import AlumnoView, GrupoView
from views.calificacionView import CalificacionView
from views.reporteView import ReporteView

# 👈 AGREGAR reporte_controller como parámetro
def MenuView(page, alumno_controller, grupo_controller, estadisticas_controller, calificacion_controller, reporte_controller):
    VINO_PRINCIPAL = "#722F37"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    user = page.session.get("user")
    nombre_usuario = user.get("nombre", "Docente") if user else "Docente"

    # Crear las vistas
    vista_alumnos = AlumnoView(page, alumno_controller)
    vista_grupos = GrupoView(page, grupo_controller)
    vista_calificaciones = CalificacionView(page, alumno_controller, calificacion_controller)
    # 👈 PASAR reporte_controller
    vista_reportes = ReporteView(page, alumno_controller, reporte_controller)

    # Tabs para navegar
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="📚 Alumnos", content=ft.Container(content=vista_alumnos, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="👥 Grupos", content=ft.Container(content=vista_grupos, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="📖 Calificaciones", content=ft.Container(content=vista_calificaciones, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="📋 Reportes", icon=ft.icons.DESCRIPTION, content=ft.Container(content=vista_reportes, padding=20, alignment=ft.alignment.top_center)),
        ],
        expand=True,
        indicator_color=VINO_PRINCIPAL,
    )

    return ft.View(
        route="/menu",
        bgcolor=GRIS_SUAVE,
        appbar=ft.AppBar(
            title=ft.Text(f"🎓 Bienvenido, {nombre_usuario}", color=BLANCO, size=22),
            bgcolor=VINO_PRINCIPAL,
            center_title=True,
            actions=[
                ft.IconButton(icon=ft.icons.LOGOUT, icon_color=BLANCO, on_click=lambda _: page.go("/")),
            ],
        ),
        controls=[tabs],
    )