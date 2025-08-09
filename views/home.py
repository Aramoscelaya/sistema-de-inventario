import flet as ft

def home_view(page):
    # Opciones del menú (puedes agregar más y se acomodarán automáticamente)
    opciones = [
        {"label": "Asignaciones", "icon": ft.Icons.ASSIGNMENT_ADD, "ruta": "/assignment"},
        {"label": "Mantenimientos", "icon": ft.Icons.CONSTRUCTION, "ruta": "/maintenances"},
        {"label": "Dispositivos", "icon": ft.Icons.DEVICES_OTHER_ROUNDED, "ruta": "/devices"},
        {"label": "Usuarios", "icon": ft.Icons.PEOPLE, "ruta": "/users"},
        {"label": "Reportes", "icon": ft.Icons.ASSESSMENT, "ruta": "/reports"},
        {"label": "Ayuda", "icon": ft.Icons.HELP, "ruta": "/help"},
    ]

    # Crear tarjetas tipo botón con íconos
    tarjetas = [
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(opcion["icon"], size=40),
                    ft.Text(opcion["label"], size=14, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            border_radius=12,
            padding=20,
            on_click=lambda e, ruta=opcion["ruta"]: page.go(ruta),
        )
        for opcion in opciones
    ]

    return ft.View(
        route="/",
        controls=[
            ft.Text("Control de inventario", size=30, weight=ft.FontWeight.BOLD, font_family= "bodoni"),
            ft.GridView(
                expand=True,
                runs_count=3,  # Número de columnas deseadas en pantallas normales
                max_extent=200,  # Ancho máximo por ítem
                spacing=20,
                run_spacing=20,
                controls=tarjetas,
            ),
        ]
    )
