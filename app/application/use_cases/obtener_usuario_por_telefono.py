from app.domain.entities.material import Material
from app.domain.repositories.user_repository import UserRepository

class ObtenerUsuarioPorTelefonoUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, material_id: str) -> Material:
        return self.user_repository.get_by_id(material_id)
