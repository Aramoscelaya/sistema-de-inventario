import flet as ft
from components.form_and_table import base

def usuario_view(page):
    def go_to_second(e):
        page.go("/bar_reader?redirect=maintenances")
        
    contenidoA= [
        ft.Text("Ingrese sus datos",
                size= 40,
                text_align= "center",
                font_family= "vivaldi")
    ]

    contenidoB= [
        ft.ElevatedButton("Ir a ventana secundaria", on_click=go_to_second),
    ]

    return ft.View(
        "/usuario",
        [
            ft.ResponsiveRow(
                base('Titulo Base test', contenidoA, contenidoB, page),
            )
            #ft.Text("Formulario de Usuario"),
            #ft.TextField(label="Nombre"),
            #ft.ElevatedButton("Regresar", on_click=lambda e: page.go("/"))
        ]
    )
