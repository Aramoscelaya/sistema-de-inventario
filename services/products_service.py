# Ej. obtener, crear, validar usuarios
from database import get_connection
import mysql.connector
from models.products_model import Product

def get_products_table():
    DB_CONECT = get_connection()
    cursor = DB_CONECT.cursor()
    datos = []
    try:
        cursor.execute("SELECT id_producto, num_serie, hostname, id_area, id_categoria, estatus FROM productos")  
        rows = cursor.fetchall()  # Obtiene todos los registros
        datos = [Product(id_producto=r[0], num_serie=r[1], hostname=r[2], id_area=r[3], id_categoria=r[4], estatus=r[5]) for r in rows]

        DB_CONECT.close()
    except mysql.connector.errors.ProgrammingError as e:
        print(f"❌ Error en la consulta SQL: {e}")
    except mysql.connector.Error as e:
        print(f"⚠️ Error en la conexión o ejecución: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexion' in locals() and DB_CONECT.is_connected():
            DB_CONECT.close()
            print("Conexión cerrada.")
    
    return datos

def product_by_serialnumber(serialnumber):
    DB_CONECT = get_connection()
    cursor = DB_CONECT.cursor()
    datos = []
    try:
        cursor.execute(f"SELECT * FROM productos WHERE num_serie = '{serialnumber}'")
        datos = cursor.fetchall()  # Obtiene todos los registros
        #[(9, 'PF3T77PC', 'THINKPAD L14', 'LENOVO', '', '', 0, '', 'WPHI002-LP', '', '', '', '', 1, 5, 2, datetime.datetime(2025, 6, 2, 18, 35, 55), datetime.datetime(2025, 6, 2, 18, 35, 55), 'Admin')]
        DB_CONECT.close()
    except mysql.connector.errors.ProgrammingError as e:
        print(f"❌ Error en la consulta SQL: {e}")
    except mysql.connector.Error as e:
        print(f"⚠️ Error en la conexión o ejecución: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conexion' in locals() and DB_CONECT.is_connected():
            DB_CONECT.close()
            print("Conexión cerrada.")
    
    return datos