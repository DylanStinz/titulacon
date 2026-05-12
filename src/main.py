import flet as ft
from controllers.UserController import AuthController
from controllers.TareaController import TareaController
from views.loginView import LoginView
from views.dashboardView import DashboardView
from views.registerView import RegisterView 

def start(page: ft.Page):
    auth_ctrl = AuthController()
    task_ctrl = TareaController()

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(LoginView(page, auth_ctrl))

        elif page.route == "/register": 
            page.views.append(RegisterView(page, auth_ctrl))

        elif page.route == "/dashboard":
            page.views.append(DashboardView(page, task_ctrl))

        else:
            page.views.append(
                ft.View("/", [ft.Text("Error: ruta no encontrada o vista vacía")])
            )

        top_view = page.views[-1]
        page.go(top_view.route)
        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    print("Iniciando aplicación...")
    
    if page.route == "/":
        route_change(None)
    else:
        page.go("/")

def main():
    ft.app(target=start)

if __name__ == "__main__":
    main()