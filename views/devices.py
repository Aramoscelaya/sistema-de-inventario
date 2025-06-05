import flet as ft
from database import data_table_home
from config import state_area, state_category

def device_view(page):
    datos = data_table_home()
    
    # Campo de búsqueda
    filtro = ft.TextField(label="Buscar por nombre o correo", on_change=lambda e: actualizar_tabla())

    tabla = ft.DataTable(
        width=800,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Área")),
            ft.DataColumn(ft.Text("Numero Serie")),
            ft.DataColumn(ft.Text("Tipo dispositivo")),
            ft.DataColumn(ft.Text("Hostname")),
            ft.DataColumn(ft.Text("Estatus")),
        ],
        rows=[]
    )
    
    tabla.rows.clear()  # Limpiar antes de agregar nuevos datos
    for row in datos:
        tabla.rows.append(ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(row[0]))),
                ft.DataCell(ft.Text(state_area[row[3]])),
                ft.DataCell(ft.Text(row[1])),
                ft.DataCell(ft.Text(state_category[row[4]])),
                ft.DataCell(ft.Text(row[2])),
                ft.DataCell(ft.Text(row[5])),  # Formato de precio
            ]
        ))
    page.update()

    return ft.View(
        route="/devices",
        controls=[
            ft.Text("Listado de dispositivos", size=30, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column(
                    controls=[tabla],
                    scroll="auto",
                ),
                height=400,
                expand=True,
                padding=10
            ),
            ft.ElevatedButton("Regresar", on_click=lambda e: page.go("/"))
        ]
    )