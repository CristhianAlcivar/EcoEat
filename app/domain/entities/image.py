from datetime import datetime
from uuid import UUID
from typing import Dict

class Image:
    def __init__(
        self,
        id: UUID,
        nombre_imagen: str,
        ruta: str,
        usuario_id: UUID,
        fecha: datetime,
        modelo_id: UUID 
    ):
        self.id = id
        self.nombre_imagen = nombre_imagen
        self.ruta = ruta
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.modelo_id = modelo_id
