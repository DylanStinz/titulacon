import flet as ft

# ============================================================
# VISTA DE CALIFICACIONES (CON ESTADÍSTICAS GENERALES)
# ============================================================
def CalificacionView(page, alumno_controller, calificacion_controller):
    VINO_PRINCIPAL = "#722F37"
    VINO_OSCURO = "#4A1C22"
    VINO_CLARO = "#9B4B55"
    BLANCO = "#FFFFFF"
    GRIS_SUAVE = "#FAFAFA"
    
    alumnos = alumno_controller.obtener_alumnos()
    info = ft.Column()
    estadisticas_container = ft.Column()
    
    def calcular_estadisticas_generales():
        """Calcula estadísticas de TODOS los alumnos"""
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
            return {"promedio": 0, "aprobados": 0, "reprobados": 0, "total_alumnos": len(alumnos), "total_con_calif": 0}
        
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
        stats = calcular_estadisticas_generales()
        estadisticas_container.controls = [
            ft.Container(
                padding=20,
                bgcolor=BLANCO,
                border_radius=16,
                border=ft.border.all(1, VINO_CLARO),
                content=ft.Column(
                    [
                        ft.Row([ft.Icon(ft.icons.ANALYTICS, color=VINO_PRINCIPAL), ft.Text("📊 Estadísticas Generales del Sistema", size=18, weight=ft.FontWeight.BOLD, color=VINO_OSCURO)], spacing=10),
                        ft.Divider(color=VINO_CLARO),
                        ft.Text(f"👥 Total alumnos registrados: {stats['total_alumnos']}", size=15, color=VINO_OSCURO),
                        ft.Text(f"📈 Promedio general de todos los alumnos: {stats['promedio']}", size=15, color=VINO_OSCURO),
                        ft.Row(
                            [
                                ft.Container(
                                    bgcolor="#4CAF50",
                                    border_radius=10,
                                    padding=10,
                                    width=140,
                                    content=ft.Column([ft.Icon(ft.icons.CHECK_CIRCLE, color=BLANCO), ft.Text(f"✅ Aprobados: {stats['aprobados']}", color=BLANCO)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                ),
                                ft.Container(
                                    bgcolor="#F44336",
                                    border_radius=10,
                                    padding=10,
                                    width=140,
                                    content=ft.Column([ft.Icon(ft.icons.CANCEL, color=BLANCO), ft.Text(f"❌ Reprobados: {stats['reprobados']}", color=BLANCO)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                ),
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
    
    dropdown = ft.Dropdown(
        label="Seleccionar Alumno",
        width=400,
        options=[
            ft.dropdown.Option(str(a["id_alumno"]), f'{a["nombre"]} {a["apellido_paterno"]} ({a.get("grupo", "")})')
            for a in alumnos
        ],
        border_color=VINO_PRINCIPAL,
        focused_border_color=VINO_OSCURO,
        bgcolor=BLANCO,
        border_radius=10,
    )
    
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
        promedio = round((float(p1) + float(p2) + float(p3)) / 3, 2) if calificaciones else 0
        info.controls = [
            ft.Container(
                padding=20,
                bgcolor=BLANCO,
                border_radius=16,
                border=ft.border.all(1, VINO_CLARO),
                content=ft.Column(
                    [
                        ft.Text(f"📖 Parcial 1: {p1}", size=18, color=VINO_OSCURO),
                        ft.Text(f"📖 Parcial 2: {p2}", size=18, color=VINO_OSCURO),
                        ft.Text(f"📖 Parcial 3: {p3}", size=18, color=VINO_OSCURO),
                        ft.Divider(),
                        ft.Text(f"🎯 Promedio Final: {promedio}", size=22, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
                    ],
                    spacing=15,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
        ]
        page.update()
    
    dropdown.on_change = mostrar_calificaciones_alumno
    
    # Mostrar estadísticas al cargar
    mostrar_estadisticas()
    
    # RETORNAR COLUMN, NO VIEW
    return ft.Column(
        [
            ft.Text("📖 Consulta de Calificaciones", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            estadisticas_container,
            ft.Divider(),
            dropdown,
            ft.Container(
                content=info,
                height=300,
                width=450,
            ),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )