import flet as ft
from database import get_data_user_dropdown
from components.dropdown import get_dropdown
from state import shared_data  # Importar el estado compartido
# id_asinacion, estatus, id_usuario, id_producto, fecha_creacion, fecha_modificacion, usuario_modificacion

def assignment_view(page):

    opciones = get_data_user_dropdown()
    contenedor = get_dropdown(opciones, page)

    return ft.View(
        route="/assignment",
        controls=[
            ft.Text("Asignacion de equipos", size=30),
            contenedor,
            ft.ElevatedButton("Volver", on_click=lambda e: page.go("/"))
        ],
    )