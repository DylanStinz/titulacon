import flet as ft
from views.alumnoView import AlumnoView, GrupoView
from views.calificacionView import CalificacionView
from views.reporteView import ReporteView
from views.riesgoView import RiesgoView
from views.actividadesView import ActividadesView
from controllers.ActividadController import ActividadController
from views.altaAlumnoView import AltaAlumnoView

def MenuView(page, alumno_controller, grupo_controller, estadisticas_controller, calificacion_controller, reporte_controller):
    VINO_PRINCIPAL = "#722F37"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    user = page.session.get("user")
    nombre_usuario = user.get("nombre", "Docente") if user else "Docente"

    grupo_seleccionado_text = ft.Text("Ningún grupo seleccionado", size=14, color=VINO_PRINCIPAL)

    from controllers.RiesgoController import RiesgoController
    riesgo_controller = RiesgoController()
    actividad_controller = ActividadController()

    def refrescar_todo(e):
        """Refresca todas las vistas"""
        if grupo_actual:
            if hasattr(vista_alumnos, 'cargar_alumnos_por_grupo'):
                vista_alumnos.cargar_alumnos_por_grupo(grupo_actual)
            if hasattr(vista_calificaciones, 'actualizar_por_grupo'):
                vista_calificaciones.actualizar_por_grupo(grupo_actual)
            if hasattr(vista_reportes, 'actualizar_por_grupo'):
                vista_reportes.actualizar_por_grupo(grupo_actual)
            if hasattr(vista_riesgos, 'actualizar_por_grupo'):
                vista_riesgos.actualizar_por_grupo(grupo_actual)
            if hasattr(vista_actividades, 'actualizar_por_grupo'):
                vista_actividades.actualizar_por_grupo(grupo_actual)
            if hasattr(vista_grupos, 'cargar_grupos'):
                vista_grupos.cargar_grupos()
        
        page.snack_bar = ft.SnackBar(
            ft.Text("🔄 Datos actualizados", color=ft.colors.BLACK), 
            bgcolor=ft.colors.GREY_200,
            duration=1500
        )
        page.snack_bar.open = True
        page.update()

    grupo_actual = None

    def on_grupo_seleccionado(grupo_dict):
        nonlocal grupo_actual
        grupo_actual = grupo_dict
        grupo_seleccionado_text.value = f"✅ Grupo seleccionado: {grupo_dict['grado']}° {grupo_dict['grupo']}"
        
        if hasattr(vista_alumnos, 'cargar_alumnos_por_grupo'):
            vista_alumnos.cargar_alumnos_por_grupo(grupo_dict)
        if hasattr(vista_calificaciones, 'actualizar_por_grupo'):
            vista_calificaciones.actualizar_por_grupo(grupo_dict)
        if hasattr(vista_reportes, 'actualizar_por_grupo'):
            vista_reportes.actualizar_por_grupo(grupo_dict)
        if hasattr(vista_riesgos, 'actualizar_por_grupo'):
            vista_riesgos.actualizar_por_grupo(grupo_dict)
        if hasattr(vista_actividades, 'actualizar_por_grupo'):
            vista_actividades.actualizar_por_grupo(grupo_dict)
        
        page.update()

    vista_grupos = GrupoView(page, grupo_controller, alumno_controller, on_grupo_seleccionado)
    vista_alumnos = AlumnoView(page, alumno_controller, grupo_controller)
    vista_calificaciones = CalificacionView(page, alumno_controller, calificacion_controller, grupo_controller)
    vista_reportes = ReporteView(page, alumno_controller, reporte_controller, grupo_controller)
    vista_riesgos = RiesgoView(page, riesgo_controller, alumno_controller, grupo_controller)
    vista_actividades = ActividadesView(page, actividad_controller, grupo_controller)
    vista_alta_alumno = AltaAlumnoView(page, alumno_controller, grupo_controller)
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="👥 Grupos", content=ft.Container(content=vista_grupos, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="📚 Alumnos", content=ft.Container(content=vista_alumnos, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="📖 Calificaciones", content=ft.Container(content=vista_calificaciones, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="📋 Reportes", icon=ft.icons.DESCRIPTION, content=ft.Container(content=vista_reportes, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="⚠️ Riesgo Académico", icon=ft.icons.WARNING, content=ft.Container(content=vista_riesgos, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="📝 Actividades", icon=ft.icons.ASSIGNMENT, content=ft.Container(content=vista_actividades, padding=20, alignment=ft.alignment.top_center)),
            ft.Tab(text="📝 Alta de Alumnos", icon=ft.icons.ADD, content=ft.Container(content=vista_alta_alumno, padding=20, alignment=ft.alignment.top_center)),

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
                ft.IconButton(
                    icon=ft.icons.REFRESH, 
                    icon_color=BLANCO, 
                    on_click=refrescar_todo,
                    tooltip="Refrescar datos",
                ),
                ft.IconButton(
                    icon=ft.icons.LOGOUT, 
                    icon_color=BLANCO, 
                    on_click=lambda _: page.go("/"),
                    tooltip="Cerrar sesión",
                ),
            ],
        ),
        controls=[
            ft.Column(
                [
                    ft.Row([grupo_seleccionado_text], alignment=ft.MainAxisAlignment.CENTER),
                    tabs,
                ],
                spacing=10,
                expand=True,
            )
        ],
    )