from typing import List, Dict
from app.domain.repositories.material_repository import MaterialRepository

class ObtenerMaterialesUseCase:
    def __init__(self, materials_repository: MaterialRepository):
        self.materials_repository = materials_repository

    def execute(self) -> List[Dict]:
        return self.materials_repository.list_all()
