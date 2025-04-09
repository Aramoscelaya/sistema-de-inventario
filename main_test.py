import flet as ft
import threading
from camera import get_camera, get_frame, encode_frame_to_base64
from scanner import scan_code
import cv2
import pygame
import time
import subprocess
import sys
import csv
from config import data_connection, stateArea, stateCategory
from database import create_connection, create_cursor, close_connection
import mysql.connector



cap = get_camera()
scanning = False
result_text = None
page = None
cursor = None
DB_CONECT = None

pygame.mixer.init()
sound = pygame.mixer.Sound('beep.mp3')


def scan_loop2():
    global scanning, page
    code_count = {}
    frames_checked = 0

    while scanning:
        frame = get_frame(cap)
        code = scan_code(frame)

        if code:
            if code in code_count:
                code_count[code] += 1
            else:
                code_count[code] = 1
            frames_checked += 1 

            height, width, _ = frame.shape
            cv2.rectangle(frame, (50, height - 60), 
                          (width - 50, height - 10), 
                          (0, 255, 0), -1)
            cv2.putText(frame, f"Detected: {code}", 
                        (60, height - 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, 
                        (255, 255, 255), 2)

            if frames_checked >= 10:
                for c, count in code_count.items():
                    if count >= 10:
                        result_text.value = f"Resultado: {c}"
                        getCode(c)
                        sound.play()
                        time.sleep(0.5)
                        break

                code_count.clear()
                frames_checked = 0

        page.image.src_base64 = encode_frame_to_base64(frame)
        page.update()

def getCode(code):
    codes = code[0]
    # Dividir la cadena por comas
    datos = codes.split(',')
    
    print('Este es el codigo final')
    print(datos)

def camara_main2(p: ft.Page):
    global page, result_text 
    page = p 
    page.title = "Escáner de Códigos"
    page.window.width = 800
    page.window.height = 600

    result_text = ft.Text(value="Resultado: ", size=20)
    global scanning
    scanning = True
    threading.Thread(target=scan_loop2).start()

    camera_image = ft.Image(src="0.png", width=640, height=480)
    page.image = camera_image

    page.add(
        ft.Column([
            camera_image,
            result_text,
        ], alignment=ft.MainAxisAlignment.CENTER)
    )



def main(page: ft.Page):
    opciones = [{"label":"Python", "value":"py"}, {"label":"JavaScript", "value":"js"}, {"label":"Java", "value":"jv"}, {"label":"Swift", "value":"sft"}]
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
        options=[ft.dropdown.Option(op["value"], text=op["label"]) for op in opciones],
        on_change=lambda e: on_click(e),
        width=300
    )

    def actualizar_opciones(valor):
        if valor:
            filtro = [op for op in opciones if valor.lower() in op["label"].lower()]
        else:
            filtro = opciones
        
        dropdown.options = [ft.dropdown.Option(op["value"], text=op["label"]) for op in filtro]
        page.update()

    contenedor = ft.Column([
        txt_busqueda,
        dropdown
    ])


    page.add(contenedor, texto)


def main_csv(page: ft.Page):
    page.title = "Lista de datos CSV"

    lista = ft.ListView(expand=True)

    def cargar_csv(e):
        DB_CONECT = create_connection()
        cursor = create_cursor()

        dataValue = []
        response = []
        dataInsert = []

        try:
            with open("inventario_test.csv", newline='', encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Omitir encabezados
                #INSERT INTO Inventario.productos (num_serie, nombre_producto, modelo, marca, hostname, descripcion_producto, estatus, id_area, id_categoria, usuario_modificacion)
                #VALUES ('8CCDN02', 'CPU Dell', 'optiplex 3090', '', 'WPNXT30-PC', 'PC de NXT servicios', 1, 1, 1, 'WPSIS07');
                for fila in lector_csv:
                    idArea = stateArea[fila[1]]
                    idCategoria = stateCategory[fila[5]]
                    dataInsert = [fila[3], "", fila[4], fila[2], fila[0], fila[8], 1, idArea, idCategoria, 'Admin']
                
                    print(dataInsert)
                    
                    sql = 'INSERT INTO productos (num_serie, nombre_producto, modelo, marca, hostname, descripcion_producto, estatus, id_area, id_categoria, usuario_modificacion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    valores = (dataInsert)

                    response = cursor.execute(sql, valores)
                    DB_CONECT.commit()  # Guarda los cambios en la base de datos
                    print(response)

            print("Registro insertado, ID:", cursor.lastrowid)
            close_connection()
        except mysql.connector.errors.ProgrammingError as e:
            print(f"❌ Error en la consulta SQL: {e}")
        except mysql.connector.Error as e:
            print(f"⚠️ Error en la conexión o ejecución: {e}")
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conexion' in locals() and DB_CONECT.is_connected():
                close_connection()
                print("Conexión cerrada.")
        
        page.update()
        return response


    boton_cargar = ft.ElevatedButton("Cargar CSV", on_click=cargar_csv)

    page.add(boton_cargar, lista)


ft.app(target=main_csv)
