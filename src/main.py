import flet as ft

from controllers.UserController import AuthController
from controllers.GrupoController import GrupoController

from views.loginView import LoginView
from views.grupoView import GrupoView
from views.registerView import RegisterView


def start(page: ft.Page):

    auth_ctrl = AuthController()
    grupo_ctrl = GrupoController()

    def route_change(e):

        page.views.clear()

        if page.route == "/":

            page.views.append(
                LoginView(page, auth_ctrl)
            )

        elif page.route == "/register":

            page.views.append(
                RegisterView(page, auth_ctrl)
            )

        elif page.route == "/dashboard":

            page.views.append(
                GrupoView(page, grupo_ctrl)
            )

        else:

            page.views.append(

                ft.View(

                    route="/error",

                    controls=[
                        ft.Text("Ruta no encontrada")
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

    print("Iniciando aplicación...")

    page.route = "/"

    route_change(None)


def main():

    ft.app(target=start)


if __name__ == "__main__":

    main()