import flet as ft

def CalificacionView(page, alumno_controller, calificacion_controller, grupo_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"

    info = ft.Column()
    estadisticas_container = ft.Column()
    dropdown = ft.Dropdown(
        label="Seleccionar Alumno",
        width=400,
        options=[],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=10,
    )

    grupo_actual = None

    def obtener_alumnos_grupo(grupo):
        if not grupo:
            return []
        todos = alumno_controller.obtener_alumnos()
        return [a for a in todos if str(a.get("semestre", "")) == str(grupo["grado"]) and a.get("grupo", "") == grupo["grupo"]]

    def calcular_estadisticas_grupo(grupo):
        alumnos = obtener_alumnos_grupo(grupo)
        todas_calificaciones = []
        for alumno in alumnos:
            califs = alumno_controller.obtener_calificaciones_alumno(alumno["id_alumno"])
            if califs:
                p1 = p2 = p3 = 0
                for c in califs:
                    if c["parcial"] == 1:
                        p1 = c["calificacion"]
                    elif c["parcial"] == 2:
                        p2 = c["calificacion"]
                    elif c["parcial"] == 3:
                        p3 = c["calificacion"]
                promedio = round((float(p1) + float(p2) + float(p3)) / 3, 2)
                todas_calificaciones.append(promedio)
        if not todas_calificaciones:
            return {"promedio": 0, "aprobados": 0, "reprobados": 0, "total_alumnos": len(alumnos), "total_con_calif": 0, "porcentaje": 0}
        promedio_general = round(sum(todas_calificaciones) / len(todas_calificaciones), 2)
        aprobados = sum(1 for p in todas_calificaciones if p >= 6)
        reprobados = sum(1 for p in todas_calificaciones if p < 6)
        porcentaje = round((aprobados / len(todas_calificaciones)) * 100, 1) if len(todas_calificaciones) > 0 else 0
        return {
            "promedio": promedio_general,
            "aprobados": aprobados,
            "reprobados": reprobados,
            "total_alumnos": len(alumnos),
            "total_con_calif": len(todas_calificaciones),
            "porcentaje": porcentaje
        }

    def mostrar_estadisticas():
        stats = calcular_estadisticas_grupo(grupo_actual)
        grupo_texto = f"{grupo_actual['grado']}° {grupo_actual['grupo']}" if grupo_actual else "No seleccionado"
        estadisticas_container.controls = [
            ft.Container(
                padding=20,
                bgcolor=BLANCO,
                border_radius=16,
                border=ft.border.all(1, VINO_CLARO),
                content=ft.Column(
                    [
                        ft.Row([ft.Icon(ft.icons.ANALYTICS, color=VINO_PRINCIPAL), ft.Text(f"📊 Estadísticas del Grupo {grupo_texto}", size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO)], spacing=10),
                        ft.Divider(color=VINO_CLARO),
                        ft.Text(f"👥 Total alumnos en el grupo: {stats['total_alumnos']}", size=15, color=VINO_OSCURO),
                        ft.Text(f"📈 Promedio general del grupo: {stats['promedio']}", size=15, color=VINO_OSCURO),
                        ft.Row(
                            [
                                ft.Container(bgcolor="#4CAF50", border_radius=10, padding=10, width=140, content=ft.Column([ft.Icon(ft.icons.CHECK_CIRCLE, color=BLANCO), ft.Text(f"✅ Aprobados: {stats['aprobados']}", color=BLANCO)], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                                ft.Container(bgcolor="#F44336", border_radius=10, padding=10, width=140, content=ft.Column([ft.Icon(ft.icons.CANCEL, color=BLANCO), ft.Text(f"❌ Reprobados: {stats['reprobados']}", color=BLANCO)], horizontal_alignment=ft.CrossAxisAlignment.CENTER)),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                        ft.Text(f"📊 Porcentaje de aprobación: {stats['porcentaje']}%", size=16, color=VINO_PRINCIPAL, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=12,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ]
        page.update()

    def cargar_alumnos_dropdown():
        if not grupo_actual:
            dropdown.options = []
            dropdown.value = None
            info.controls = []
            page.update()
            return
        alumnos = obtener_alumnos_grupo(grupo_actual)
        dropdown.options = [
            ft.dropdown.Option(str(a["id_alumno"]), f'{a["nombre"]} {a["apellido_paterno"]} ({a.get("grupo", "")})')
            for a in alumnos
        ]
        dropdown.value = None
        info.controls = []
        page.update()

    def mostrar_calificaciones_alumno(e):
        if not dropdown.value:
            return
        calificaciones = calificacion_controller.obtener_calificaciones(dropdown.value)
        p1 = p2 = p3 = 0
        for c in calificaciones:
            if c["parcial"] == 1:
                p1 = c["calificacion"]
            elif c["parcial"] == 2:
                p2 = c["calificacion"]
            elif c["parcial"] == 3:
                p3 = c["calificacion"]
        calificaciones_validas = [float(x) for x in [p1, p2, p3] if float(x) > 0]
        promedio = round(sum(calificaciones_validas) / len(calificaciones_validas), 2) if calificaciones_validas else 0
        p1_mostrar = "Pendiente" if float(p1) == 0 else p1
        p2_mostrar = "Pendiente" if float(p2) == 0 else p2
        p3_mostrar = "Pendiente" if float(p3) == 0 else p3
        estado = "⏳ En proceso" if len(calificaciones_validas) < 3 else ("✅ Aprobado" if promedio >= 6 else "❌ Reprobado")
        info.controls = [
            ft.Container(
                padding=20,
                bgcolor=BLANCO,
                border_radius=16,
                border=ft.border.all(1, VINO_CLARO),
                content=ft.Column(
                    [
                        ft.Text(f"📖 Parcial 1: {p1_mostrar}", size=18, color=VINO_OSCURO),
                        ft.Text(f"📖 Parcial 2: {p2_mostrar}", size=18, color=VINO_OSCURO),
                        ft.Text(f"📖 Parcial 3: {p3_mostrar}", size=18, color=VINO_OSCURO),
                        ft.Divider(),
                        ft.Text(f"🎯 Promedio Actual: {promedio}", size=22, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
                        ft.Text(estado, size=20, weight=ft.FontWeight.BOLD, color="#4CAF50" if "Aprobado" in estado else ("#F44336" if "Reprobado" in estado else "#FF9800")),
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ]
        page.update()

    dropdown.on_change = mostrar_calificaciones_alumno

    def actualizar_por_grupo(grupo):
        nonlocal grupo_actual
        grupo_actual = grupo
        mostrar_estadisticas()
        cargar_alumnos_dropdown()

    content = ft.Column(
        [
            ft.Text("📖 Consulta de Calificaciones", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            estadisticas_container,
            ft.Divider(),
            dropdown,
            ft.Container(content=info, height=300, width=450),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    container = ft.Container(content=content)
    container.actualizar_por_grupo = actualizar_por_grupo
    return container