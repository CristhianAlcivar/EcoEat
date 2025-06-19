from datetime import datetime
from uuid import uuid4, UUID

class User:
    def __init__(self, telefono: str, id: UUID = None, registro: datetime = None):
        self.id = id or uuid4()
        self.telefono = telefono
        self.registro = registro or datetime.utcnow()
