from datetime import datetime
from uuid import UUID

class User:
    def __init__(self, id: UUID, telefono: str, registro: datetime):
        self.id = id
        self.telefono = telefono
        self.registro = registro
