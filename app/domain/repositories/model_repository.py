from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.domain.entities.model_performance import ModelPerformance

class ModelRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[ModelPerformance]:
        pass

    @abstractmethod
    def get_by_id(self, model_id: UUID) -> ModelPerformance:
        pass
