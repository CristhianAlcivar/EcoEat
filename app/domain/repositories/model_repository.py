from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.models import Models

class ModelRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Models]:
        """Devuelve todos los modelos."""
        pass

    @abstractmethod
    def get_best_model(self) -> Optional[Models]:
        """Devuelve el modelo con mayor precisión."""
        pass

    @abstractmethod
    def get_by_id(self, model_id: UUID) -> Optional[Models]:
        """Obtiene un modelo por su ID."""
        pass

    @abstractmethod
    def save(self, model: Models) -> None:
        """Guarda un modelo nuevo en la base de datos."""
        pass

    @abstractmethod
    def update(self, model_id: UUID, **kwargs) -> None:
        """Actualiza los datos de un modelo existente."""
        pass

    @abstractmethod
    def delete(self, model_id: UUID) -> None:
        """Elimina un modelo por su ID."""
        pass
