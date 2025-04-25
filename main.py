import flet as ft
#import threading
from camera import get_camera, get_frame, encode_frame_to_base64, start_scan, close_camera
from scanner import scan_code
from components.alert import alert_dialog
from components.dropdown import get_dropdown
#import cv2
#import pygame
#import time
from database import data_table_home, get_data_user_dropdown
#from products import
import config


#scanning = False
result_text = None
page = None

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

def home(page):
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
    )

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
    page.title = "Dropdown en Flet"

    # Lista de opciones dinámicas
    opciones = get_data_user_dropdown()
    contenedor = get_dropdown(opciones, page)
    page.add(contenedor, alert_dialog(page))

#ft.app(target=main, view=ft.WEB_BROWSER)
#ft.app(target=main, view=ft.FLET_APP)
ft.app(target=main)