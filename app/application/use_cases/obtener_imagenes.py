from typing import List, Dict
from app.domain.repositories.image_repository import ImageRepository

class ObtenerImagenesUseCase:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self) -> List[Dict]:
        return self.image_repository.get_all_with_user()
