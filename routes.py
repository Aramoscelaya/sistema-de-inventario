from views.home import home_view
from views.assignment import assignment_view
from views.users import usuario_view
#from views.productos import productos_view
#from views.usuarios import usuarios_view
#from views.reportes import reportes_view
from views.not_found import not_found_view

def route_handler(page):
    page.views.clear()

    ruta = page.route

    if ruta == "/":
        page.views.append(home_view(page))
    elif ruta == "/assignment":
        page.views.append(assignment_view(page))
    elif ruta == "/maintenances":
        page.views.append(not_found_view(page))
    elif ruta == "/reports":
        page.views.append(not_found_view(page))
    elif ruta == "/devices":
        page.views.append(not_found_view(page))
    elif ruta == "/users":
        page.views.append(usuario_view(page))
    elif ruta == "/help":
        page.views.append(not_found_view(page))
    else:
        # Ruta no válida
        page.views.append(not_found_view(page))

    page.update()
