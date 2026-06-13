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
                validas = [x for x in [p1, p2, p3] if x > 0]
                if validas:
                    promedio = round(sum(validas) / len(validas), 2)
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
                        ft.Text(f"📊 Porcentaje de aprobación: {stats.get('porcentaje', 0)}%", size=16, color=VINO_PRINCIPAL, weight=ft.FontWeight.BOLD),
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

    def guardar_calificacion(alumno_id, parcial, valor):
        try:
            if valor and float(valor) >= 0:
                nueva_calif = min(float(valor), 10)
                calificacion_controller.actualizar_calificacion(alumno_id, parcial, nueva_calif)
                return True
        except Exception as ex:
            print(f"Error: {ex}")
        return False

    def mostrar_calificaciones_alumno(e):
        if not dropdown.value:
            return
        
        alumno_id = int(dropdown.value)
        calificaciones = alumno_controller.obtener_calificaciones_alumno(alumno_id)
        
        p1 = p2 = p3 = 0.0
        for c in calificaciones:
            if c["parcial"] == 1:
                p1 = float(c["calificacion"])
            elif c["parcial"] == 2:
                p2 = float(c["calificacion"])
            elif c["parcial"] == 3:
                p3 = float(c["calificacion"])
        
        calificaciones_validas = [x for x in [p1, p2, p3] if x > 0]
        promedio = round(sum(calificaciones_validas) / len(calificaciones_validas), 2) if calificaciones_validas else 0
        
        p1_mostrar = "" if p1 == 0 else str(p1)
        p2_mostrar = "" if p2 == 0 else str(p2)
        p3_mostrar = "" if p3 == 0 else str(p3)
        
        estado = "⏳ En proceso" if len(calificaciones_validas) < 3 else ("✅ Aprobado" if promedio >= 6 else "❌ Reprobado")
        estado_color = "#FF9800" if len(calificaciones_validas) < 3 else ("#4CAF50" if promedio >= 6 else "#F44336")
        
        p1_field = ft.TextField(
            label="Parcial 1",
            value=p1_mostrar,
            width=120,
            border_color=VINO_PRINCIPAL,
            focused_border_color=VINO_OSCURO,
            bgcolor=BLANCO,
            border_radius=10,
            filled=True,
            fill_color=GRIS_SUAVE,
            suffix_text="/10",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*\.?[0-9]?$"),
        )
        
        p2_field = ft.TextField(
            label="Parcial 2",
            value=p2_mostrar,
            width=120,
            border_color=VINO_PRINCIPAL,
            focused_border_color=VINO_OSCURO,
            bgcolor=BLANCO,
            border_radius=10,
            filled=True,
            fill_color=GRIS_SUAVE,
            suffix_text="/10",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*\.?[0-9]?$"),
        )
        
        p3_field = ft.TextField(
            label="Parcial 3",
            value=p3_mostrar,
            width=120,
            border_color=VINO_PRINCIPAL,
            focused_border_color=VINO_OSCURO,
            bgcolor=BLANCO,
            border_radius=10,
            filled=True,
            fill_color=GRIS_SUAVE,
            suffix_text="/10",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*\.?[0-9]?$"),
        )
        
        promedio_text = ft.Text(f"🎯 Promedio: {promedio}", size=22, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL)
        estado_text = ft.Text(estado, size=20, weight=ft.FontWeight.BOLD, color=estado_color)
        
        def on_guardar(e):
            alumno_id_int = int(dropdown.value)
            if p1_field.value and p1_field.value != p1_mostrar:
                guardar_calificacion(alumno_id_int, 1, p1_field.value)
            if p2_field.value and p2_field.value != p2_mostrar:
                guardar_calificacion(alumno_id_int, 2, p2_field.value)
            if p3_field.value and p3_field.value != p3_mostrar:
                guardar_calificacion(alumno_id_int, 3, p3_field.value)
            
            page.snack_bar = ft.SnackBar(ft.Text("✅ Calificaciones guardadas", color=ft.colors.BLACK), bgcolor=ft.colors.GREY_200)
            page.snack_bar.open = True
            
            # Recargar todo
            mostrar_calificaciones_alumno(None)
            mostrar_estadisticas()
            page.update()
        
        info.controls = [
            ft.Container(
                padding=20,
                bgcolor=BLANCO,
                border_radius=16,
                border=ft.border.all(1, VINO_CLARO),
                content=ft.Column(
                    [
                        ft.Row([p1_field, p2_field, p3_field], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
                        ft.ElevatedButton(
                            "💾 Guardar calificaciones",
                            on_click=on_guardar,
                            icon=ft.icons.SAVE,
                            style=ft.ButtonStyle(
                                color=BLANCO,
                                bgcolor=VINO_PRINCIPAL,
                                shape=ft.RoundedRectangleBorder(radius=20),
                            ),
                        ),
                        ft.Divider(),
                        promedio_text,
                        estado_text,
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
            ft.Text("📖 Consulta y Edición de Calificaciones", size=30, weight=ft.FontWeight.BOLD, color=VINO_PRINCIPAL),
            ft.Divider(),
            estadisticas_container,
            ft.Divider(),
            dropdown,
            ft.Container(content=info, width=500),
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    container = ft.Container(content=content)
    container.actualizar_por_grupo = actualizar_por_grupo
    return container