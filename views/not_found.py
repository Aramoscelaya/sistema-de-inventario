import flet as ft

def not_found_view(page):
    return ft.View(
        route="/404",
        controls=[
            ft.Text("404 - Página no encontrada", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Volver al inicio", on_click=lambda e: page.go("/"))
        ]
    )
