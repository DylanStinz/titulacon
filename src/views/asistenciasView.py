import flet as ft
from datetime import date

def AsistenciasView(page, alumno_controller, grupo_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    grupo_actual = None
    alumnos_data = []  # lista de (dropdown, id_alumno)

    fecha_picker = ft.DatePicker()
    page.overlay.append(fecha_picker)

    # Selectores con tamaño más amplio
    dropdown_materia = ft.Dropdown(
        label="Materia",
        width=300,
        options=[],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=10,
        filled=True,
        fill_color=GRIS_SUAVE,
    )
    txt_fecha = ft.TextField(
        label="Fecha",
        width=180,
        read_only=True,
        value=date.today().strftime("%Y-%m-%d"),
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=10,
    )
    btn_fecha = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, icon_size=24, on_click=lambda e: fecha_picker.pick_date())

    estado_global = ft.Dropdown(
        label="Aplicar a todos",
        width=220,
        options=[
            ft.dropdown.Option("Asistió"),
            ft.dropdown.Option("Falta"),
            ft.dropdown.Option("Retardo"),
        ],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=10,
        filled=True,
        fill_color=GRIS_SUAVE,
    )
    btn_aplicar_todos = ft.ElevatedButton(
        "Aplicar a todos",
        icon=ft.icons.SELECT_ALL,
        on_click=lambda e: aplicar_estado_todos(),
        style=ft.ButtonStyle(color=BLANCO, bgcolor=VINO_PRINCIPAL),
        height=42,
    )

    # Tabla de alumnos con tamaños más grandes
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Alumno", weight=ft.FontWeight.BOLD, color=VINO_OSCURO, size=14)),
            ft.DataColumn(ft.Text("Matrícula", weight=ft.FontWeight.BOLD, color=VINO_OSCURO, size=14)),
            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, color=VINO_OSCURO, size=14)),
        ],
        column_spacing=30,
        heading_row_height=50,
        data_row_max_height=50,
        rows=[],
        border=ft.border.all(1, VINO_CLARO),
        border_radius=10,
        horizontal_lines=ft.BorderSide(1, VINO_CLARO),
    )

    def cargar_materias():
        materias = grupo_controller.obtener_materias()
        opciones = [ft.dropdown.Option(str(m["id_materia"]), m["nombre_materia"]) for m in materias]
        dropdown_materia.options = opciones
        if opciones:
            dropdown_materia.value = opciones[0].key
        page.update()

    def cargar_alumnos():
        if not grupo_actual:
            data_table.rows = []
            page.update()
            return
        todos = alumno_controller.obtener_alumnos()
        filtrados = [a for a in todos if str(a.get("semestre", "")) == str(grupo_actual["grado"]) and a.get("grupo", "") == grupo_actual["grupo"] and a.get("estatus", "Activo") == "Activo"]
        
        rows = []
        alumnos_data.clear()
        for alumno in filtrados:
            estado_dropdown = ft.Dropdown(
                width=160,
                options=[
                    ft.dropdown.Option("Asistió"),
                    ft.dropdown.Option("Falta"),
                    ft.dropdown.Option("Retardo"),
                ],
                border_color=VINO_PRINCIPAL,
                focused_border_color=VINO_OSCURO,
                bgcolor=BLANCO,
                border_radius=8,
                filled=True,
                fill_color=GRIS_SUAVE,
            )
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{alumno['nombre']} {alumno['apellido_paterno']}", size=14)),
                        ft.DataCell(ft.Text(alumno['matricula'], size=14, color=VINO_CLARO)),
                        ft.DataCell(estado_dropdown),
                    ]
                )
            )
            alumnos_data.append((estado_dropdown, alumno["id_alumno"]))
        data_table.rows = rows
        page.update()

    def aplicar_estado_todos():
        if not estado_global.value:
            page.snack_bar = ft.SnackBar(ft.Text("Selecciona un estado primero"), bgcolor=GRIS_SUAVE)
            page.snack_bar.open = True
            page.update()
            return
        for estado_dropdown, _ in alumnos_data:
            estado_dropdown.value = estado_global.value
        page.update()

    def guardar_asistencias(e):
        if not dropdown_materia.value or not txt_fecha.value:
            page.snack_bar = ft.SnackBar(ft.Text("Selecciona materia y fecha"), bgcolor=GRIS_SUAVE)
            page.snack_bar.open = True
            page.update()
            return
        if not alumnos_data:
            page.snack_bar = ft.SnackBar(ft.Text("No hay alumnos en este grupo"), bgcolor=GRIS_SUAVE)
            page.snack_bar.open = True
            page.update()
            return

        id_materia = int(dropdown_materia.value)
        fecha = fecha_picker.value if fecha_picker.value else date.today()
        if hasattr(fecha, 'date'):
            fecha = fecha.date()

        guardados = 0
        for estado_dropdown, id_alumno in alumnos_data:
            if estado_dropdown.value:
                alumno_controller.crear_asistencia(id_alumno, fecha, estado_dropdown.value, id_materia)
                guardados += 1

        page.snack_bar = ft.SnackBar(ft.Text(f"✅ {guardados} asistencias guardadas"), bgcolor=GRIS_SUAVE)
        page.snack_bar.open = True
        page.update()
        # Limpiar selección de estados
        for estado_dropdown, _ in alumnos_data:
            estado_dropdown.value = None
        estado_global.value = None
        page.update()

    def fecha_change(e):
        if fecha_picker.value:
            txt_fecha.value = fecha_picker.value.strftime("%Y-%m-%d")
            page.update()

    fecha_picker.on_change = fecha_change

    def actualizar_por_grupo(grupo):
        nonlocal grupo_actual
        grupo_actual = grupo
        cargar_materias()
        cargar_alumnos()

    # Layout
    content = ft.Column(
        [
            ft.Text("📋 Gestión de Asistencias por Grupo", size=28, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            ft.Row(
                [dropdown_materia, txt_fecha, btn_fecha],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            ft.Row(
                [estado_global, btn_aplicar_todos],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=25,
            ),
            ft.Divider(),
            ft.Text("Lista de alumnos", size=20, weight=ft.FontWeight.BOLD, color=VINO_OSCURO),
            ft.Container(
                content=ft.Column([data_table], scroll=ft.ScrollMode.AUTO),
                height=500,
                padding=10,
            ),
            ft.Row(
                [ft.ElevatedButton("💾 Guardar todas las asistencias", on_click=guardar_asistencias, icon=ft.icons.SAVE, bgcolor=VINO_PRINCIPAL, color=BLANCO, height=45, width=280)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=25,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    container = ft.Container(content=content)
    container.actualizar_por_grupo = actualizar_por_grupo
    return container