import flet as ft
from datetime import datetime

def ActividadesView(page, actividad_controller, grupo_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_MUY_SUAVE = "#FAFAFA"

    estilo_textfield = {
        "border_color": VINO_PRINCIPAL,
        "focused_border_color": VINO_OSCURO,
        "cursor_color": VINO_PRINCIPAL,
        "bgcolor": BLANCO,
        "border_radius": 12,
        "filled": True,
        "fill_color": GRIS_MUY_SUAVE,
    }

    grupo_actual = None
    lista_actividades = ft.Column(spacing=15)

    titulo = ft.TextField(label="Título", width=400, **estilo_textfield)
    descripcion = ft.TextField(label="Descripción", multiline=True, min_lines=3, max_lines=5, width=400, **estilo_textfield)
    fecha_limite = ft.TextField(label="Fecha límite (YYYY-MM-DD)", width=200, **estilo_textfield)
    asignatura = ft.TextField(label="Asignatura (opcional)", width=200, **estilo_textfield)

    actividad_editando = {"id": None}

    def actualizar_por_grupo(grupo_dict):
        nonlocal grupo_actual
        grupo_actual = grupo_dict
        cargar_actividades()
        page.update()

    def cargar_actividades():
        lista_actividades.controls.clear()
        if not grupo_actual:
            lista_actividades.controls.append(ft.Text("Selecciona un grupo para ver sus actividades", italic=True, color=VINO_PRINCIPAL))
            page.update()
            return

        actividades = actividad_controller.obtener_actividades_por_grupo(grupo_actual["id_grupo"])
        if not actividades:
            lista_actividades.controls.append(ft.Text("No hay actividades registradas para este grupo", italic=True, color=VINO_PRINCIPAL))
        else:
            for act in actividades:
                lista_actividades.controls.append(crear_tarjeta_actividad(act))
        page.update()

    def crear_tarjeta_actividad(act):
        def editar(e):
            titulo.value = act["titulo"]
            descripcion.value = act["descripcion"]
            fecha_limite.value = act["fecha_limite"] if act["fecha_limite"] else ""
            asignatura.value = act["asignatura"] or ""
            actividad_editando["id"] = act["id_actividad"]
            page.update()

        def eliminar(e):
            ok, msg = actividad_controller.eliminar_actividad(act["id_actividad"])
            page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=BLANCO, behavior=ft.SnackBarBehavior.FLOATING)
            page.snack_bar.open = True
            if ok:
                cargar_actividades()
            page.update()

        return ft.Container(
            width=500,
            border_radius=16,
            bgcolor=BLANCO,
            shadow=ft.BoxShadow(blur_radius=8, color="#D3D3D3", offset=ft.Offset(0, 2)),
            border=ft.border.all(1, VINO_CLARO),
            padding=15,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(act["titulo"], size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
                                    ft.Text(act["descripcion"], size=14, color=VINO_PRINCIPAL),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.DATE_RANGE, size=14, color=VINO_PRINCIPAL),
                                            ft.Text(f"Límite: {act['fecha_limite'] or 'Sin fecha'}", size=12),
                                            ft.Icon(ft.icons.BOOK, size=14, color=VINO_PRINCIPAL),
                                            ft.Text(f"Asignatura: {act['asignatura'] or 'General'}", size=12),
                                        ],
                                        spacing=5,
                                    ),
                                ],
                                spacing=5,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.IconButton(ft.icons.EDIT, icon_color=VINO_PRINCIPAL, on_click=editar),
                                    ft.IconButton(ft.icons.DELETE, icon_color=VINO_CLARO, on_click=eliminar),
                                ],
                                spacing=0,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                ]
            ),
        )

    def guardar_actividad(e):
        if not grupo_actual:
            page.snack_bar = ft.SnackBar(ft.Text("Primero selecciona un grupo"), bgcolor=BLANCO, behavior=ft.SnackBarBehavior.FLOATING)
            page.snack_bar.open = True
            page.update()
            return

        if not titulo.value:
            page.snack_bar = ft.SnackBar(ft.Text("El título es obligatorio"), bgcolor=BLANCO, behavior=ft.SnackBarBehavior.FLOATING)
            page.snack_bar.open = True
            page.update()
            return

        fecha_val = fecha_limite.value.strip() if fecha_limite.value else None
        if fecha_val:
            try:
                datetime.strptime(fecha_val, "%Y-%m-%d")
            except ValueError:
                page.snack_bar = ft.SnackBar(ft.Text("Formato de fecha inválido. Usa YYYY-MM-DD"), bgcolor=BLANCO)
                page.snack_bar.open = True
                page.update()
                return

        if actividad_editando["id"]:
            ok, msg = actividad_controller.actualizar_actividad(
                actividad_editando["id"],
                titulo.value,
                descripcion.value,
                fecha_val,
                asignatura.value,
            )
            actividad_editando["id"] = None
        else:
            ok, msg = actividad_controller.crear_actividad(
                grupo_actual["id_grupo"],
                titulo.value,
                descripcion.value,
                fecha_val,
                asignatura.value,
            )

        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=BLANCO, behavior=ft.SnackBarBehavior.FLOATING)
        page.snack_bar.open = True
        if ok:
            titulo.value = ""
            descripcion.value = ""
            fecha_limite.value = ""
            asignatura.value = ""
            cargar_actividades()
        page.update()

    return ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                padding=ft.padding.symmetric(horizontal=40, vertical=20),
                content=ft.Column(
                    [
                        ft.Text("Gestión de Actividades por Grupo", size=28, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
                        ft.Container(
                            padding=20,
                            bgcolor=BLANCO,
                            border_radius=20,
                            shadow=ft.BoxShadow(blur_radius=8, color="#D3D3D3", offset=ft.Offset(0, 2)),
                            content=ft.Column(
                                [
                                    ft.Row([titulo, asignatura], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                                    descripcion,
                                    ft.Row([fecha_limite], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.ElevatedButton(
                                        "Guardar actividad",
                                        width=200,
                                        on_click=guardar_actividad,
                                        style=ft.ButtonStyle(color=BLANCO, bgcolor=VINO_PRINCIPAL, shape=ft.RoundedRectangleBorder(radius=30)),
                                    ),
                                ],
                                spacing=20,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ),
                        ft.Divider(color=VINO_CLARO, height=2, thickness=1),
                        ft.Text("Actividades del grupo seleccionado", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
                        lista_actividades,
                    ],
                    spacing=25,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ],
    )