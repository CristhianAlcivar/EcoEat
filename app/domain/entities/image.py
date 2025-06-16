from datetime import datetime
from uuid import UUID
from typing import Dict

class Image:
    def __init__(self, id: UUID, nombre_imagen: str, ruta: str,
                 usuario_id: UUID, fecha: datetime,
                 resultado_modelo: Dict, materiales_renovables: int,
                 materiales_no_renovables: int, confianza_promedio: float):
        self.id = id
        self.nombre_imagen = nombre_imagen
        self.ruta = ruta
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.resultado_modelo = resultado_modelo
        self.materiales_renovables = materiales_renovables
        self.materiales_no_renovables = materiales_no_renovables
        self.confianza_promedio = confianza_promedio
