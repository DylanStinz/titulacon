import flet as ft

def DashboardView(page, tarea_controller):

    user = getattr(page.session, "user", None)

    if not user:
        page.go("/")
        return ft.View(route="/", controls=[])

    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    def refresh():
        lista_tareas.controls.clear()
        for t in tarea_controller.obtener_lista(user["id"]):
            lista_tareas.controls.append(
                ft.Text(t["titulo"]) 
            )
        page.update()

    txt_titulo = ft.TextField(label="Nueva Tarea", expand=True)

    def add_task(e):
        success, msg = tarea_controller.guardar_nueva(
            user["id"], txt_titulo.value, "", "Media", "trabajo"
        )
        if success:
            txt_titulo.value = ""
            refresh()


    refresh()

    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(title=ft.Text(f"Bienvenido, {user['nombre']}")),
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Row([
                        txt_titulo,
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD,
                            on_click=add_task
                        )
                    ]),
                    ft.Divider(),
                    lista_tareas
                ], expand=True)
            )
        ]
    )


def logout(page):
    page.session.user = None
    page.go("/")