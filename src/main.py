import flet as ft
from controllers.AlumnoController import AlumnoController
from controllers.EstadisticasController import EstadisticasController
from controllers.UserController import AuthController
from controllers.GrupoController import GrupoController
from controllers.CalificacionController import CalificacionController
from controllers.ReporteController import ReporteController  # 👈 IMPORTAR

from views.loginView import LoginView
from views.registerView import RegisterView
from views.menuView import MenuView

def start(page: ft.Page):
    page.title = "Sistema de Gestión Escolar"
    page.theme_mode = ft.ThemeMode.LIGHT

    auth_ctrl = AuthController()
    alumno_ctrl = AlumnoController()
    grupo_ctrl = GrupoController()
    estadisticas_ctrl = EstadisticasController()
    calificacion_ctrl = CalificacionController()
    reporte_ctrl = ReporteController()  # 👈 CREAR

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(LoginView(page, auth_ctrl))
        elif page.route == "/register":
            page.views.append(RegisterView(page, auth_ctrl))
        elif page.route == "/menu" or page.route == "/dashboard":
            # 👈 PASAR reporte_ctrl
            page.views.append(MenuView(page, alumno_ctrl, grupo_ctrl, estadisticas_ctrl, calificacion_ctrl, reporte_ctrl))
        else:
            page.views.append(
                ft.View(
                    route="/error",
                    controls=[
                        ft.Text("Ruta no encontrada", size=30),
                        ft.ElevatedButton("Volver al inicio", on_click=lambda _: page.go("/"))
                    ]
                )
            )
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

def main():
    ft.app(target=start)

if __name__ == "__main__":
    main()