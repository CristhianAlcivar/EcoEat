from app.domain.entities.model_performance import ModelPerformance
from app.domain.repositories.model_repository import ModelRepository
from app.data.db.models import ModelPerformanceModel
from app.data.db.database import SessionLocal
from uuid import UUID

class SQLAlchemyModelRepository(ModelRepository):
    def list_all(self) -> list[ModelPerformance]:
        with SessionLocal() as session:
            records = session.query(ModelPerformanceModel).all()
            return [ModelPerformance(
                modelo_id=r.modelo_id,
                nombre=r.nombre,
                formato=r.formato,
                score=r.score,
                precision=r.precision,
                recall=r.recall,
                dataset=r.dataset,
                fecha_entrenamiento=r.fecha_entrenamiento,
                optimizado=r.optimizado
            ) for r in records]

    def get_by_id(self, model_id: UUID) -> ModelPerformance:
        with SessionLocal() as session:
            r = session.query(ModelPerformanceModel).filter(ModelPerformanceModel.modelo_id == model_id).first()
            if not r:
                return None
            return ModelPerformance(
                modelo_id=r.modelo_id,
                nombre=r.nombre,
                formato=r.formato,
                score=r.score,
                precision=r.precision,
                recall=r.recall,
                dataset=r.dataset,
                fecha_entrenamiento=r.fecha_entrenamiento,
                optimizado=r.optimizado
            )
