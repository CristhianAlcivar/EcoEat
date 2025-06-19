from typing import List
from app.domain.entities.models import ModelPerformance
from app.domain.repositories.model_repository import ModelRepository

class ListarModelosEntrenadosUseCase:
    def __init__(self, model_repository: ModelRepository):
        self.model_repository = model_repository

    def execute(self) -> List[ModelPerformance]:
        return self.model_repository.list_all()
