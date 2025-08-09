import flet as ft
from state import shared_data  # Importar el estado compartido
from components.overlay import overlay_action
from config import state_maintenance, state_category
from services.maintenance_service import create_maintenances, get_maintenance_table, get_by_id, obtener_mantenimientos

def maintenances_view(page):
    overlay, mostrar_espera = overlay_action(page)
    page.run_thread(mostrar_espera)
    datos = get_maintenance_table()
    options_status = [
        {'label': 'Pendiente', 'value': 1},
        {'label': 'Diagnóstico', 'value': 2},
        {'label': 'En curso', 'value': 3},
        {'label': 'Preventivo', 'value': 4},
        {'label': 'Correctivo', 'value': 5},
        {'label': 'En observación', 'value': 6},
        {'label': 'Listo', 'value': 7}
    ]

    tabla = ft.DataTable(
        width=800,
        columns=[
            #ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("Dispositivo")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Ultima modificacion")),
            ft.DataColumn(ft.Text("Editar")),
        ],
        rows=[]
    )
    tabla.rows.clear()  # Limpiar antes de agregar nuevos datos
    for row in datos:
        tabla.rows.append(ft.DataRow(
            cells=[
                #ft.DataCell(ft.Text(str(row[0]))),
                ft.DataCell(ft.Text(row[2])),
                ft.DataCell(ft.Text(state_category[row[3]])),
                ft.DataCell(ft.Text(state_maintenance[row[1]])),
                ft.DataCell(ft.Text(row[4].strftime("%d/%m/%Y"))),
                ft.DataCell(
                    ft.IconButton(icon=ft.Icons.EDIT, tooltip="Edit", on_click=lambda e, id= row[0]: page.go(f"/maintenances_edit?id={id}"))
                ),
            ]
        ))
    page.update()

    def go_to_second(e):
        page.go("/bar_reader?redirect=maintenances")

    def search_maintenances(e):
        page.go("/search_maintenances")

    mensaje_out = ft.Text("", size=14)
    campos = {
        "txt_value": ft.Text(f"SN: {shared_data["value"]}", size=20),
        "descripcion_manto": ft.TextField(label="Descripción", max_length=100, multiline=True,width=400),
        "estado_manto": ft.Dropdown(label="Elige una opción", options=[ft.dropdown.Option(op["value"], text=op["label"]) for op in options_status], width=300),
    }

    return ft.View(
        route="/maintenances",
        controls=[
            ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text("Mantenimiento de equipos", size=30, weight=ft.FontWeight.BOLD, font_family="bodoni"),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.IconButton(icon=ft.Icons.HOME, tooltip="Home", on_click=lambda e: page.go("/")),
                            #content=ft.ElevatedButton("Volver al inicio", on_click=lambda e: page.go("/")),
                            alignment=ft.alignment.center,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ),
            ]),
            #ft.ElevatedButton("Buscar mantenimiento", on_click=search_maintenances),
            ft.ResponsiveRow(
                expand=True,
                controls = [
                    ft.Container(
                        bgcolor = "#222222",
                        border_radius = 10,
                        col = 4,
                        expand=True,
                        content= ft.Column(
                            controls= [
                                ft.ElevatedButton("Ir a ventana secundaria", on_click=lambda e: go_to_second(e)),
                                *campos.values(),
                                ft.ElevatedButton("Enviar", on_click=lambda e: enviar_formulario(e, campos, page, mensaje_out)),
                                mensaje_out
                            ]
                        )
                    ),
                    ft.Container(
                        bgcolor = "#222222",
                        border_radius = 10,
                        col = 8,
                        expand=True,
                        content= ft.Column(
                            controls= [
                                ft.Text("Mantenimientos activos", size= 30, text_align= "center", font_family= "bodoni"),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[tabla],
                                        scroll="auto",
                                    ),
                                    height=400,
                                    expand=True,
                                    padding=5
                                ),
                            ]
                        )
                    )
                ]
            ),
            #overlay,
        ],
        padding=20
    )

def enviar_formulario(e, campos, page, mensaje_out):
    errores = []

    # Validaciones
    if not (campos["estado_manto"].value or "").strip():
        errores.append("El estado es un campo obligatorio")
    if not (campos["descripcion_manto"].value or "").strip():
        errores.append("La descripcion es un campo obligatorio")
    if not (shared_data["value"] or "").strip():
        errores.append("El numero de serie es un campo obligatorio")

    # Si hay errores, mostrar y salir
    if errores:
        mensaje_out.value = "\n".join(errores)
        mensaje_out.color = ft.Colors.RED
        page.update()
        return

    # Enviar datos
    try:
        mensaje_out.value = " "
        producto = {
            "descripcion_manto": campos["descripcion_manto"].value.strip(),
            "estado_manto": campos["estado_manto"].value.strip(),
            "txt_value": shared_data["value"]
        }

        resultMantenance = create_maintenances(producto)  # función backend

        mensaje_out.value = resultMantenance
        mensaje_out.color = ft.Colors.GREEN

        # Limpiar campos
        for c in campos.values():
            c.value = ""

    except Exception as ex:
        mensaje_out.value = f"Error al guardar: {str(ex)}"
        mensaje_out.color = ft.Colors.RED

    page.update()

def search_maintenances(page):
    return ft.View(
        route="/search_maintenances",
        controls=[
            ft.Text("Busqueda de Mantenimiento", size=30, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Volver", on_click=lambda e: page.go("/maintenances")),
        ],
        padding=20
    )
    
def maintenances_edit(page, id):
    overlay, mostrar_espera = overlay_action(page)
    options_status = [
        {'label': 'Pendiente', 'value': 1},
        {'label': 'Diagnóstico', 'value': 2},
        {'label': 'En curso', 'value': 3},
        {'label': 'Preventivo', 'value': 4},
        {'label': 'Correctivo', 'value': 5},
        {'label': 'En observación', 'value': 6},
        {'label': 'Listo', 'value': 7}
    ]
    data = get_by_id(id)
    page.run_thread(mostrar_espera)

    #mensaje_out = ft.Text("", size=14)
    campos = {
        "txt_value": ft.Text(f"SN: {data[0][2]}", size=20),
        "descripcion_manto": ft.TextField(label="Descripción", max_length=100, multiline=True,width=400),
        "estado_manto": ft.Dropdown(label="Elige una opción", options=[ft.dropdown.Option(op["value"], text=op["label"]) for op in options_status], width=300),
    }

    campos["descripcion_manto"].value = data[0][3]
    campos["estado_manto"].value = data[0][1]
    page.update()
    
    return ft.View(
        route="/maintenances_edit",
        controls=[
            ft.Column([
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text("Editar mantenimiento", size=30, weight=ft.FontWeight.BOLD, font_family="bodoni"),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton("Volver", on_click=lambda e: page.go("/maintenances")),
                            alignment=ft.alignment.center,
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ),
            ]),
            ft.ResponsiveRow(
                expand=True,
                controls = [
                    ft.Container(
                        bgcolor = "#222222",
                        border_radius = 10,
                        col = 5,
                        expand=True,
                        content= ft.Column(
                            controls=[
                                *campos.values(),
                                ft.ElevatedButton("Enviar", on_click=lambda e: enviar_formulario(e, campos, page, mensaje_out)),
                            ]
                        )
                    )
                ]
            ),
            #overlay,
        ],
        padding=20
    )
