# Ej. obtener, crear, validar usuarios
from database import get_connection
import mysql.connector
from models.maintenance_model import Maintenance
from services.products_service import product_by_serialnumber
from models.maintenance_model import Maintenance


def create_maintenances(data):
    DB_CONECT = get_connection()
    cursor = DB_CONECT.cursor()
    response = []
    try:
        productSearch = product_by_serialnumber(data['txt_value'])

        if not productSearch:
            DB_CONECT.close()
            return "❌ Producto no encontrado"
        
        mantenanceSearch = maintenance_by_id_product(productSearch[0][0])

        if mantenanceSearch:
            if not mantenanceSearch[0][1] == 7:
                DB_CONECT.close()
                return "❌ Producto con mantenimiento pendiente"
        else:
            msj = ""
            try:
                sql = 'INSERT INTO mantenimientos (estado_manto, descripcion_manto, estatus, id_producto, usuario_modificacion) VALUES (%s, %s, %s, %s, %s)'
                valores = ([int(data['estado_manto']), data['descripcion_manto'], 1, productSearch[0][0], 'Admin'])
                cursor.execute(sql, valores)
                DB_CONECT.commit()  # Guarda los cambios en la base de datos

                if cursor.rowcount > 0:
                    msj = "✅ Mantenimiento agregado"
                else:
                    msj = "⚠️ Mantenimiento no generado"

            except mysql.connector.Error as err:
                print("❌ Error de MySQL:", err)

            DB_CONECT.close()
            return msj
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
    
    return response

def maintenance_by_id_product(id):
    DB_CONECT = get_connection()
    cursor = DB_CONECT.cursor()
    datos = []
    try:
        cursor.execute(f"SELECT * FROM mantenimientos WHERE id_producto = '{id}'")
        datos = cursor.fetchall()  # Obtiene todos los registros
        
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

def obtener_mantenimientos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_mantenimiento, estado_manto, descripcion_manto FROM mantenimientos")
    filas = cursor.fetchall()
    conn.close()
    
    return [Maintenance(id_mantenimiento=f[0], estado_manto=f[1], descripcion_manto=f[2]) for f in filas]

def get_maintenance_table():
    DB_CONECT = get_connection()
    cursor = DB_CONECT.cursor()
    datos = []
    try:
        cursor.execute("SELECT m.id_mantenimiento, m.estado_manto, p.num_serie, p.id_categoria, m.fecha_modificacion FROM mantenimientos AS m INNER JOIN productos AS p ON p.id_producto = m.id_producto WHERE m.estado_manto != 7")  
        rows = cursor.fetchall()  # Obtiene todos los registros
        #datos = [Maintenance(id_mantenimiento=r[0], estado_manto=r[1], id_producto=r[2], fecha_modificacion=r[3]) for r in rows]

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
    
    return rows

def get_by_id(id):
    DB_CONECT = get_connection()
    cursor = DB_CONECT.cursor()
    datos = []
    try:
        cursor.execute("SELECT m.id_mantenimiento, m.estado_manto, p.num_serie, m.descripcion_manto, m.fecha_modificacion FROM mantenimientos AS m INNER JOIN productos AS p ON p.id_producto = m.id_producto WHERE m.id_mantenimiento = "+id)
        rows = cursor.fetchall()  # Obtiene todos los registros

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
    
    return rows

