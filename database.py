import threading
#import psycopg2
from config import data_connection, stateArea, stateCategory
import mysql.connector
import datetime
import json

cursor = None
DB_CONECT = None

def create_connection():
    try:
        global DB_CONECT
        
        DB_CONECT = mysql.connector.connect(
            host = data_connection['host'],
            user = data_connection['user'],
            password = data_connection['password'],
            database = data_connection['database']
        )
        print("✅ Conexión exitosa")
        return DB_CONECT

    except mysql.connector.Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return False
    finally:
        if 'conexion' in locals() and DB_CONECT.is_connected():
            DB_CONECT.close()

def create_cursor():
    global cursor
    cursor = DB_CONECT.cursor()

    if not cursor:
        raise Exception("No se puso crear el cursor Msql.")
    return cursor

def close_connection():
    if DB_CONECT.is_connected():
        # Cierra la conexión al finalizar
        DB_CONECT.close()
        print("✅ Conexión cerrada a MySQL")

def guardar_codigo(codigo):
    pass#thread = threading.Thread(target=insertar_codigo, args=(codigo))
    #thread.start()

def create_product(data):
    create_connection()
    create_cursor()
    #[{'name': 'num_serie', 'value': 'PF4HD0K'}, {'name': 'modelo', 'value': 'E14'}, {'name': 'marca', 'value': 'Lenovo'}, {'name': 'hostname', 'value': 'WPHI002-LP'}, {'name': 'id_area', 'value': 'Honest'}, {'name': 'id_categoria', 'value': 'Laptop'}, {'name': 'usuario_modificacion', 'value': 'admin'}]
    dataName = []
    dataValue = []
    response = []

    try:
        for items in data:
            dataName.append(items['name'])
            if items['name'] == 'id_area':
                value = stateArea[items['value']]
                dataValue.append(value)
            elif items['name'] == 'id_categoria':
                value = stateCategory[items['value']]
                dataValue.append(value)
            else:
                dataValue.append(items['value'])

        sql = 'INSERT INTO productos (nombre_producto, '+', '.join(dataName)+') VALUES ("", %s, %s, %s, %s, %s, %s, %s)'
        valores = (dataValue)

        print(sql)
        print(valores)

        response = cursor.execute(sql, valores)
        DB_CONECT.commit()  # Guarda los cambios en la base de datos

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
    return response

def data_table_home():
    create_connection()
    create_cursor()
    datos = []
    try:
        cursor.execute("SELECT id_producto, num_serie, hostname FROM productos")  
        datos = cursor.fetchall()  # Obtiene todos los registros
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
    
    return datos
    
def get_data_user_dropdown():
    create_connection()
    create_cursor()
    datos = []
    try:
        cursor.execute("SELECT id_usuario, usuario, nombre FROM usuarios")  
        datas = cursor.fetchall()  # Obtiene todos los registros
        for data in datas:
            item = {}
            item['label'] = data[1]
            item['value'] = data[2]
            datos.append(item)

        print(datos)
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
    
    return datos
'''
def insertar_codigo(codigo):
    cursor = DB_CONECT.cursor()

    queryIfExist = "SELECT EXISTS (SELECT 1 FROM barcodes WHERE barcode = %s)"
    cursor.execute(queryIfExist, (codigo))
    
    if not cursor:
        query = "INSERT INTO barcodes (barcode, registered_at) VALUES (%s, %s)"
        
        try:
            cursor.execute(query, (codigo, datetime.datetime.now()))
            DB_CONECT.commit()
            print(f"Código {codigo} guardado correctamente.")
        except Exception as e:
            print(f"Error al guardar el código: {e}")
        finally:
            cursor.close()
            DB_CONECT.close()
    else:
        print(f"Código {codigo} existente.")
'''