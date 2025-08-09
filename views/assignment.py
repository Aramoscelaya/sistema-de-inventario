import flet as ft
from database import get_data_user_dropdown
from components.dropdown import get_dropdown
from state import shared_data  # Importar el estado compartido
# id_asinacion, estatus, id_usuario, id_producto, fecha_creacion, fecha_modificacion, usuario_modificacion

def assignment_view(page):

    #id_producto = ft.TextField(label="Dispositivo", width=300)
    txt_value = ft.Text(f"SN: {shared_data["value"]}", size=20)

    def go_to_second(e):
        page.go("/bar_reader?redirect=assignment")

    opciones = get_data_user_dropdown()
    contenedor = get_dropdown(opciones, page)

    resultado = ft.Text("")

    def enviar_formulario(e):
        resultado.value = f"Enviado: "
        page.update()

    return ft.View(
        route="/assignment",
        controls=[
            ft.Text("Asignacion de equipos", size=30),
            ft.ElevatedButton("Ir a ventana secundaria", on_click=go_to_second),
            txt_value,
            resultado,
            ft.ElevatedButton("Enviar", on_click=enviar_formulario),
            contenedor,
            ft.ElevatedButton("Volver", on_click=lambda e: page.go("/"))
        ],
    )