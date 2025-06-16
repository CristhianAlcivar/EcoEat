from app.domain.entities.image import Image
from app.domain.repositories.image_repository import ImageRepository
from app.data.db.models import ImageModel
from app.data.db.database import SessionLocal
from uuid import UUID

class SQLAlchemyImageRepository(ImageRepository):
    def save(self, image: Image) -> None:
        with SessionLocal() as session:
            model = ImageModel(
                id=image.id,
                nombre_imagen=image.nombre_imagen,
                ruta=image.ruta,
                usuario_id=image.usuario_id,
                fecha=image.fecha,
                resultado_modelo=image.resultado_modelo,
                materiales_renovables=image.materiales_renovables,
                materiales_no_renovables=image.materiales_no_renovables,
                confianza_promedio=image.confianza_promedio
            )
            session.add(model)
            session.commit()

    def get_by_user(self, user_id: UUID) -> list[Image]:
        with SessionLocal() as session:
            records = session.query(ImageModel).filter(ImageModel.usuario_id == user_id).all()
            return [Image(
                id=r.id,
                nombre_imagen=r.nombre_imagen,
                ruta=r.ruta,
                usuario_id=r.usuario_id,
                fecha=r.fecha,
                resultado_modelo=r.resultado_modelo,
                materiales_renovables=r.materiales_renovables,
                materiales_no_renovables=r.materiales_no_renovables,
                confianza_promedio=r.confianza_promedio
            ) for r in records]
