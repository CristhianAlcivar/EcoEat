from typing import List
from uuid import UUID
from app.domain.entities.image import Image
from app.domain.repositories.image_repository import ImageRepository

class ObtenerImagenesPorUsuarioUseCase:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, user_id: UUID) -> List[Image]:
        return self.image_repository.get_by_user(user_id)
