import flet as ft
#from database import data_table_home
from services.products_service import get_products_table
from config import state_area, state_category

def device_view(page):
    datos = get_products_table()
    
    # Campo de búsqueda
    #filtro = ft.TextField(label="Buscar por nombre o correo", on_change=lambda e: actualizar_tabla())

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
                ft.DataCell(ft.Text(str(row.id_producto))),
                ft.DataCell(ft.Text(state_area[row.id_area])),
                ft.DataCell(ft.Text(row.num_serie)),
                ft.DataCell(ft.Text(state_category[row.id_categoria])),
                ft.DataCell(ft.Text(row.hostname)),
                ft.DataCell(ft.Text(row.estatus)),  # Formato de precio
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