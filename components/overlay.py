import flet as ft
import time

def overlay_action(page: ft.Page):
    overlay = ft.Container(
        bgcolor=ft.Colors.with_opacity(.1, ft.Colors.BLACK),
        content=ft.Column(
            [
                ft.ProgressRing(),
                ft.Text("Cargando...", color=ft.Colors.WHITE)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        visible=False,
        width=page.window.width,
        height=page.window.height
    )
    def mostrar_espera():
        overlay.visible = True
        page.update()
        page.run_thread(tarea_larga)
    def tarea_larga():
        time.sleep(3)  # Simula proceso
        overlay.visible = False
        page.update()
    
    return overlay, mostrar_espera
    #page.run_thread(mostrar_espera)