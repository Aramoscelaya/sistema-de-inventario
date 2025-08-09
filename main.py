import flet as ft
from routes import route_handler

#import threading
from camera import get_camera, get_frame, encode_frame_to_base64, start_scan, close_camera
from scanner import scan_code
from components.alert import alert_dialog
from components.dropdown import get_dropdown
#import cv2
#import pygame
#import time
#from database import data_table_home, get_data_user_dropdown
#from products import
import config



#scanning = False
result_text = None
page = None
# Dato compartido entre páginas (puede ser una clase o variable global)
shared_data = {"value": ""}

#pygame.mixer.init()
#sound = pygame.mixer.Sound('beep.mp3')

def camara_main(p: ft.Page):
    global page, result_text 
    page = p 
    page.title = "Escáner de Códigos"
    page.window.width = 800
    page.window.height = 700

    result_text = ft.Text(value="Resultado: ", size=20)
    #scan_button = ft.ElevatedButton(text="Scan", on_click=start_scan)
    start_scan(e="")

    camera_image = ft.Image(src="0.png", width=640, height=450)
    page.image = camera_image

    page.add(
        ft.Column([
            camera_image,
            #scan_button,
            result_text,
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "App con Navegación Lateral"
    page.window.width = 800
    page.window.height = 650
    
    def cambiar_pagina(seccion = ""):
        page.controls.clear()  # 🔹 Limpia la página antes de cambiar de sección

        match seccion:
            case 'inicio':
                close_camera()
                home(page)
            case 'add_items':
                add_items(page)
            case 'assignment':
                close_camera()
                assignment(page)
            case _:
                home(page)
    
        page.drawer.open = False  # Cierra el menú lateral después de seleccionar
        page.update()

    contenedor_default = ft.Container(
        content=home(page),
        padding=10,
    )

    # Agregarlo a la página
    page.add(contenedor_default)

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(height=20),  # Espacio antes de los botones
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.HOME), ft.Text("Inicio")]),
                #selected=True,
                padding=10,
                on_click=lambda e: cambiar_pagina("inicio"),
            ),
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.ASSIGNMENT_ADD), ft.Text("Asignaciones")]),
                padding=10,
                on_click=lambda e: cambiar_pagina("assignment"),
            ),
            ft.Container(
                content=ft.Row([ft.Icon(ft.Icons.PLAYLIST_ADD), ft.Text("Agregar equipos")]),
                padding=10,
                on_click=lambda e: cambiar_pagina("add_items"),
            ),
        ]
    )

    # Barra superior con el botón de menú
    page.appbar = ft.AppBar(
        title=ft.Text("Inventariado"),
        leading=ft.ElevatedButton(" ",icon=ft.Icons.MENU, bgcolor=ft.Colors.BLUE_GREY_500, on_click=lambda e: page.open(drawer)),
        center_title=True,
        bgcolor=ft.Colors.BLUE_GREY_500,
    )

    page.update()

"""def home(page):
    datos = data_table_home()
    tabla = ft.DataTable(
        width=700,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Numero Serie")),
            ft.DataColumn(ft.Text("Hostname")),
        ],
        rows=[]
    )
    tabla.rows.clear()  # Limpiar antes de agregar nuevos datos
    for row in datos:
        tabla.rows.append(ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(row[0]))),
                ft.DataCell(ft.Text(row[1])),
                ft.DataCell(ft.Text(row[2])),  # Formato de precio
            ]
        ))
    page.update()

    page.add(
        ft.Column([
            ft.Text("Historial de dispositivos", size=20, weight=ft.FontWeight.BOLD),
            tabla
        ],
        scroll="always",  # 🔥 Esto habilita el scroll correctamente
        expand=True)
    )"""

def print_global_variable():
    print(config.global_variable_test)
    page.add(ft.Text(value=f"Resultado: {config.global_variable_test}", size=20))
    page.update()

def add_items(p: ft.Page):
    global page, result_text 
    page = p 
    page.title = "Escáner de Códigos"

    result_text = ft.Text(value="Resultado: ", size=20)
    start_scan(page, result_text, 'add_items', e="")

    camera_image = ft.Image(src="0.png", width=640, height=450)
    page.image = camera_image
    
    page.update(ft.Text(value=f"Resultado: {config.global_variable_test}", size=20))
    #print_global_variable()

    page.add(
        ft.Column([
            camera_image,
            #scan_button,
            result_text,
        ], alignment=ft.MainAxisAlignment.CENTER)
    )

def assignment(p: ft.Page):
    '''global page, result_text 
    page = p 
    page.title = "Escáner de Códigos"

    result_text = ft.Text(value="Resultado: ", size=20)
    start_scan(page, result_text, 'assignment', e="")

    camera_image = ft.Image(src="0.png", width=640, height=450)
    page.image = camera_image

    page.add(
        ft.Column([
            camera_image,
            #scan_button,
            result_text,
        ], alignment=ft.MainAxisAlignment.CENTER)
    )'''
    global page 
    page = p 
    page.title = "Asignaciones - equipos"


    # Función para navegar entre páginas
    def route_change(route):
        #page.views.clear()
        if page.route == "/":
            page.views.append(main_view())
        elif page.route == "/second":
            page.views.append(second_view())
        page.update()

     # Vista principal
    def main_view():
        txt_value = ft.Text(shared_data["value"], size=20)

        def go_to_second(e):
            page.go("/second")

        return ft.View(
            route="/",
            controls=[
                ft.Text("Ventana principal", size=30),
                txt_value,
                ft.ElevatedButton("Ir a ventana secundaria", on_click=go_to_second),
            ],
        )

    # Vista secundaria
    def second_view():
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
            ],
        )

    page.on_route_change = route_change
    page.go("/")

    # Lista de opciones dinámicas
    #opciones = get_data_user_dropdown()
    #contenedor = get_dropdown(opciones, page)
    #page.add(contenedor, alert_dialog(page))

def main_routes(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.title = "Control de inventariado"
    page.window.width = 1050
    page.window.height = 650

    page.on_route_change = lambda route: route_handler(page)
    page.go("/")


# Simulación de datos (esto normalmente vendría de una BD)
PRODUCTOS = {
    "1": {"nombre": "Laptop Dell", "precio": "15000"},
    "2": {"nombre": "Mouse Logitech", "precio": "500"},
    "3": {"nombre": "Monitor Samsung", "precio": "3000"},
}

def main_edit(page: ft.Page):

    nombre_field = ft.TextField(label="Nombre", width=300)
    precio_field = ft.TextField(label="Precio", width=300)

    def guardar_cambios(e, producto_id):
        PRODUCTOS[producto_id]["nombre"] = nombre_field.value
        PRODUCTOS[producto_id]["precio"] = precio_field.value
        page.go("/")  # Regresar al inicio

    def mostrar_lista():
        page.views.clear()
        lista = []
        for producto_id, datos in PRODUCTOS.items():
            lista.append(
                ft.Row(
                    [
                        ft.Text(f"{datos['nombre']} - ${datos['precio']}"),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar",
                            on_click=lambda e, pid=producto_id: page.go(f"/editar/{pid}")
                        )
                    ]
                )
            )
        lista.append(
            ft.Row(
                [
                    ft.Text(f"LAP TEST - $10000"),
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        tooltip="Editar",
                        on_click=lambda e: page.go(f"/editar/4")
                    )
                ]
            )
        )
        page.views.append(ft.View("/", controls=lista))
        page.update()

    def mostrar_edicion(producto_id):
        producto = PRODUCTOS.get(producto_id)
        if not producto:
            page.snack_bar = ft.SnackBar(ft.Text("Producto no encontrado"))
            page.snack_bar.open = True
            page.go("/")
            return

        nombre_field.value = producto["nombre"]
        precio_field.value = producto["precio"]

        page.views.clear()
        page.views.append(
            ft.View(
                f"/editar/{producto_id}",
                [
                    ft.Text(f"Editar producto ID: {producto_id}", size=20),
                    nombre_field,
                    precio_field,
                    ft.ElevatedButton("Guardar", on_click=lambda e: guardar_cambios(e, producto_id)),
                    ft.ElevatedButton("Cancelar", on_click=lambda e: page.go("/"))
                ]
            )
        )
        page.update()

    def route_change(e):
        route_parts = page.route.strip("/").split("/")
        if route_parts[0] == "":
            mostrar_lista()
        elif route_parts[0] == "editar" and len(route_parts) > 1:
            mostrar_edicion(route_parts[1])
        else:
            mostrar_lista()

    page.on_route_change = route_change
    page.go(page.route)

import time

def main_espera(page: ft.Page):
    overlay = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
        content=ft.Column(
            [
                ft.ProgressRing(),
                ft.Text("Cargando...", color=ft.Colors.WHITE)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        visible=False,
        expand=True,
    )

    def mostrar_espera():
        overlay.visible = True
        page.update()
        page.run_thread(tarea_larga)

    def tarea_larga():
        time.sleep(3)  # Simula proceso
        overlay.visible = False
        page.update()

    page.add(
        ft.Stack(
            [
                ft.Column([ft.ElevatedButton("Iniciar proceso", on_click=lambda e: mostrar_espera())]),
                overlay
            ]
        )
    )



#ft.app(target=main, view=ft.WEB_BROWSER)
#ft.app(target=main, view=ft.FLET_APP)
#ft.app(target=main)
ft.app(target=main_routes)