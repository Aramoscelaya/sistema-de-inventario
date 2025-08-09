from views.home import home_view
from views.assignment import assignment_view
from views.users import usuario_view
from views.devices import device_view
from views.maintenances import maintenances_view, search_maintenances, maintenances_edit
#from views.reportes import reportes_view
from views.bar_reader import bar_reader_view
#from views.maintenances import search_maintenances
from views.not_found import not_found_view
from urllib.parse import urlparse, parse_qs

def route_handler(page):
    page.views.clear()

    ruta = page.route

    parsed_url = urlparse(ruta)
    path = parsed_url.path              # /bar_reader
    query_params = parse_qs(parsed_url.query)

    '''if path == "/bar_reader":
        redirect = query_params.get("redirect", [""])[0]
        page.views.clear()
        page.views.append(bar_reader_view(page, redirect))'''

    match path:
        case "/":
            page.views.append(home_view(page))
        case "/assignment":
            page.views.append(assignment_view(page))
        case "/maintenances":
            page.views.append(maintenances_view(page))
        case "/maintenances_edit":
            id = query_params.get("id", [""])[0]
            page.views.clear()
            page.views.append(maintenances_edit(page, id))
        case "/reports":
            page.views.append(not_found_view(page))
        case "/devices":
            page.views.append(device_view(page))
        case "/users":
            page.views.append(usuario_view(page))
        case "/help":
            page.views.append(not_found_view(page))
        case "/search_maintenances":
            page.views.append(search_maintenances(page))
        case "/bar_reader":
            redirect = query_params.get("redirect", [""])[0]
            page.views.clear()
            page.views.append(bar_reader_view(page, redirect))
        case _:
            # Ruta no válida
            page.views.append(not_found_view(page))

    page.update()
