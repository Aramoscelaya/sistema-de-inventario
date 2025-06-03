import flet as ft
from state import shared_data  # Importar el estado compartido

def assignment_view(page):
    input_text = ft.TextField(label="Escribe algo")

    def send_data(e):
        shared_data["value"] = input_text.value
        page.go("/")  # volver a principal

    return ft.View(
        route="/second",
        controls=[
            ft.Text("Ventana secundaria", size=30),
            input_text,
            ft.ElevatedButton("Enviar a principal", on_click=send_data),
            ft.ElevatedButton("Volver", on_click=lambda e: page.go("/"))
        ],
    )