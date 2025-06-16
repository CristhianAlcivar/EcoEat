from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.material import Material

class MaterialRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Material]:
        pass

    @abstractmethod
    def get_by_id(self, material_id: str) -> Material:
        pass
