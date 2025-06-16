from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from uuid import uuid4
from datetime import datetime, timezone


class TelefonoYaRegistrado(Exception):
    pass

class RegistrarUsuarioUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, telefono: str, fecha_registro: datetime = None) -> User:
        
        if self.user_repository.get_by_telefono(telefono):
            raise TelefonoYaRegistrado("El teléfono ya está registrado.")
        
        if fecha_registro is None:
            fecha_registro = datetime.now(timezone.utc)
        user = User(id=uuid4(), telefono=telefono, registro=fecha_registro)
        self.user_repository.save(user)
        return user 