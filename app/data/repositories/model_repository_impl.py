from app.domain.entities.models import Models
from app.domain.repositories.model_repository import ModelRepository
from app.data.db.models import ModelPerformanceModel
from app.data.db.database import SessionLocal
from uuid import UUID, uuid4

class SQLAlchemyModelRepository(ModelRepository):
    def __init__(self, session=None):
        self.session = session or SessionLocal()

    def list_all(self) -> list[Models]:
        records = self.session.query(ModelPerformanceModel).all()
        return [
            Models(
                id=r.id,
                nombre=r.nombre,
                formato=r.formato,
                score=r.score,
                precision=r.precision,
                recall=r.recall,
                dataset=r.dataset,
                fecha_entrenamiento=r.fecha_entrenamiento,
                optimizado=r.optimizado
            )
            for r in records
        ]

    def get_by_id(self, model_id: UUID) -> Models | None:
        r = self.session.query(ModelPerformanceModel).filter(ModelPerformanceModel.id == model_id).first()
        if not r:
            return None
        return ModelPerformanceModel(
            id=r.id,
            nombre=r.nombre,
            formato=r.formato,
            score=r.score,
            precision=r.precision,
            recall=r.recall,
            dataset=r.dataset,
            fecha_entrenamiento=r.fecha_entrenamiento,
            optimizado=r.optimizado
        )

    def save(self, model: Models) -> Models:
        # Asume que el id es opcional y lo genera aquí si es necesario
        if not model.id:
            model.id = uuid4()
        new_model = ModelPerformanceModel(
            id=model.id,
            nombre=model.nombre,
            formato=model.formato,
            score=model.score,
            precision=model.precision,
            recall=model.recall,
            dataset=model.dataset,
            fecha_entrenamiento=model.fecha_entrenamiento,
            optimizado=model.optimizado,
        )
        self.session.add(new_model)
        self.session.commit()
        return model
    
    def get_best_model(self) -> Models | None:
        r = (
            self.session.query(ModelPerformanceModel)
            .order_by(ModelPerformanceModel.precision.desc())
            .first()
        )
        if not r:
            return None
        return Models(
            id=r.id,
            nombre=r.nombre,
            formato=r.formato,
            score=r.score,
            precision=r.precision,
            recall=r.recall,
            dataset=r.dataset,
            fecha_entrenamiento=r.fecha_entrenamiento,
            optimizado=r.optimizado
        )

    def update(self, model_id: UUID, updated_data: dict) -> Models | None:
        r = self.session.query(ModelPerformanceModel).filter(ModelPerformanceModel.id == model_id).first()
        if not r:
            return None

        # Actualizar solo atributos válidos
        for key, value in updated_data.items():
            if hasattr(r, key) and value is not None:
                setattr(r, key, value)

        self.session.commit()
        return self.get_by_id(model_id)  # esto ya devuelve un objeto Models


    def delete(self, model_id: UUID) -> bool:
        r = self.session.query(ModelPerformanceModel).filter(ModelPerformanceModel.id == model_id).first()
        if not r:
            return False
        self.session.delete(r)
        self.session.commit()
        return True
