"""DB_CONFIG = {
    "host": "149.50.136.78",
    "port": 5432,
    "database": "barcode_db",
    "user": "root",
    "password": "1234"
}

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "darksus",
    "user": "darksus",
    "password": ""
}


conn = psycopg2.connect(**DB_CONFIG)
print("--------------------------------------------------------------------------")
print(conn)
print("--------------------------------------------------------------------------")
return
"""

# config.py
global_variable_test = None

data_connection = {
    'host': "localhost",      # Cambia si usas un servidor remoto
    'user': "root",     # Usuario de MySQL
    'password': "0666", # Contraseña de MySQL
    'database': "Inventario" # Nombre de la base de datos
}


stateArea = {
    'Nexus': 1,
    'Nexus_servicio': 2,
    'Crew_support': 3,
    'B2B': 4,
    'Honest': 5,
    'Avis': 6,
    'W2FLY': 7,
    'Administracion': 8
}

stateCategory = {
    'CPU': 1,
    'Laptop': 2,
    'Monitor': 3,
    'Mini_CPU': 4,
    'UPS': 5,
}

state_area = {
    1 : 'Nexus',
    2 : 'Nexus_servicio',
    3 : 'Crew_support',
    4 : 'B2B',
    5 : 'Honest',
    6 : 'Avis',
    7 : 'W2FLY',
    8 : 'Administracion'
}

state_category = {
    1 : 'CPU',
    2 : 'Laptop',
    3 : 'Monitor',
    4 : 'Mini_CPU',
    5 : 'UPS'
}