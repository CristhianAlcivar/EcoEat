from app.domain.entities.material import Material
from app.domain.repositories.material_repository import MaterialRepository

class ObtenerMaterialPorIdUseCase:
    def __init__(self, material_repository: MaterialRepository):
        self.material_repository = material_repository

    def execute(self, material_id: str) -> Material:
        return self.material_repository.get_by_id(material_id)
