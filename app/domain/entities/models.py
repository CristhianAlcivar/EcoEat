from datetime import datetime
from uuid import UUID, uuid4

class Models:
    def __init__(
        self,
        nombre: str,
        formato: str,
        score: float,
        precision: float,
        recall: float,
        dataset: str,
        fecha_entrenamiento: datetime,
        optimizado: bool,
        id: UUID = None
    ):
        self.id = id or uuid4()
        self.nombre = nombre
        self.formato = formato
        self.score = score
        self.precision = precision
        self.recall = recall
        self.dataset = dataset
        self.fecha_entrenamiento = fecha_entrenamiento
        self.optimizado = optimizado
