# (Opcional) Estructuras de datos
from dataclasses import dataclass

@dataclass
class Maintenance:
    id_mantenimiento: int = None
    estado_manto: int = None
    descripcion_manto: str = ""
    estatus: int = None
    id_producto: int = None
    fecha_creacion: str = ""
    fecha_modificacion: str = ""
    usuario_modificacion: str = ""