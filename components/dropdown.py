import flet as ft

def get_dropdown(opciones, page: ft.Page):
    texto = ""

    txt_busqueda = ft.TextField(
        hint_text="Escribe para buscar...",
        on_change=lambda e: actualizar_opciones(e.control.value)
    )

    texto = ft.Text("Action clicked: ")

    def on_click(e):
        nonlocal texto  # Permite modificar la variable de la función superior

        if texto in page.controls:
            page.controls.remove(texto)
            page.update()
        texto = ft.Text(f"Action clicked: {e.control.value}")
        page.add(texto)

    dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(op["label"], text=op["value"]) for op in opciones],
        on_change=lambda e: on_click(e),
        width=300
    )

    def actualizar_opciones(valor):
        if valor:
            filtro = [op for op in opciones if valor.lower() in op["value"].lower()]
        else:
            filtro = opciones
        
        dropdown.options = [ft.dropdown.Option(op["label"], text=op["value"]) for op in filtro]
        page.update()

    return ft.Column([
        txt_busqueda,
        dropdown
    ])