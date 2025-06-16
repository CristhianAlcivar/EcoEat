from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.domain.entities.image import Image

class ImageRepository(ABC):
    @abstractmethod
    def save(self, image: Image) -> None:
        pass

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> List[Image]:
        pass
