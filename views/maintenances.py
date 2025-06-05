import flet as ft
from state import shared_data  # Importar el estado compartido

def maintenances_view(page):
# id_mantenimiento, estado_manto, descripcion_manto, estatus, id_producto, fecha_creacion, fecha_modificacion, usuario_modificacion
    options_status = [
        {'label': 'Pendiente', 'value': 1},
        {'label': 'Diagnóstico', 'value': 2},
        {'label': 'En curso', 'value': 3},
        {'label': 'Preventivo', 'value': 4},
        {'label': 'Correctivo', 'value': 5},
        {'label': 'En observación', 'value': 6},
        {'label': 'Listo', 'value': 7}
    ]

    #id_producto = ft.TextField(label="Dispositivo", width=300)
    txt_value = ft.Text(shared_data["value"], size=20)
    def go_to_second(e):
        page.go("/bar_reader")

    estado_manto = ft.Dropdown(
        label="Elige una opción",
        options=[ft.dropdown.Option(op["value"], text=op["label"]) for op in options_status],
        width=300
    )
    
    descripcion_manto = ft.TextField(
        label="Descripción",
        max_length=100,
        multiline=True,  # Opcional: para permitir varias líneas
        width=400
    )
    
    resultado = ft.Text("")

    def enviar_formulario(e):
        resultado.value = f"Enviado: {descripcion_manto.value} - {estado_manto.value}"
        page.update()

    return ft.View(
        route="/maintenances",
        controls=[
            ft.Text("Mantenimiento de equipos", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Ir a ventana secundaria", on_click=go_to_second),
            estado_manto,
            descripcion_manto,
            txt_value,
            ft.ElevatedButton("Enviar", on_click=enviar_formulario),
            resultado,
            ft.ElevatedButton("Volver al inicio", on_click=lambda e: page.go("/")),
        ],
        padding=20
    )