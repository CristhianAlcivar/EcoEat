from datetime import datetime
from uuid import UUID

class ModelPerformance:
    def __init__(self, modelo_id: UUID, nombre: str, formato: str,
                 score: float, precision: float, recall: float,
                 dataset: str, fecha_entrenamiento: datetime,
                 optimizado: bool):
        self.modelo_id = modelo_id
        self.nombre = nombre
        self.formato = formato
        self.score = score
        self.precision = precision
        self.recall = recall
        self.dataset = dataset
        self.fecha_entrenamiento = fecha_entrenamiento
        self.optimizado = optimizado
