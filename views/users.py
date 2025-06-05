import flet as ft

def usuario_view(page):
    return ft.View(
        "/usuario",
        [
            ft.Text("Formulario de Usuario"),
            ft.TextField(label="Nombre"),
            ft.ElevatedButton("Regresar", on_click=lambda e: page.go("/"))
        ]
    )
