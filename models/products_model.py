# (Opcional) Estructuras de datos
from dataclasses import dataclass

@dataclass
class Product:
    id_producto: int = None
    num_serie: str = ""
    modelo: str = ""
    marca: str = ""
    procesador: str = ""
    generacion: str = ""
    ram: int = None
    almacenamiento: str = ""
    hostname: str = ""
    tamano: str = ""
    relacion_aspecto: str = ""
    entradas: str = ""
    descripcion_producto: str = ""
    estatus: int = None
    id_area: int = None
    id_categoria: int = None