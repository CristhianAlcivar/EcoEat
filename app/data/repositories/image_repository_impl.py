from app.domain.entities.image import Image
from app.domain.repositories.image_repository import ImageRepository
from app.data.db.models import ImageModel, UserModel
from app.data.db.database import SessionLocal
from typing import List, Dict
from uuid import UUID

class SQLAlchemyImageRepository(ImageRepository):
    def __init__(self, session):
        self.session = session

    def save(self, image: Image) -> None:
        model = ImageModel(
            id=image.id,
            nombre_imagen=image.nombre_imagen,
            ruta=image.ruta,
            usuario_id=image.usuario_id,
            fecha=image.fecha,
            modelo_id=image.modelo_id  
        )
        self.session.add(model)
        self.session.commit()

    def get_by_user(self, user_id: UUID) -> list[Image]:
        records = self.session.query(ImageModel).filter(ImageModel.usuario_id == user_id).all()
        return [
            Image(
                id=r.id,
                nombre_imagen=r.nombre_imagen,
                ruta=r.ruta,
                usuario_id=r.usuario_id,
                fecha=r.fecha,
                modelo_id=r.modelo_id 
            )
            for r in records
        ]

    def get_all_with_user(self, telefono: str = None):
        query = (
            self.session.query(ImageModel, UserModel)
            .join(UserModel, UserModel.id == ImageModel.usuario_id)
        )
        if telefono:
            query = query.filter(UserModel.telefono == telefono)
        resultados = []
        for img, user in query.all():
            resultados.append({
                "id_imagen": str(img.id),
                "nombre_imagen": img.nombre_imagen,
                "usuario_id": str(user.id),
                "telefono": user.telefono,
                "ruta": img.ruta,
                "fecha": img.fecha,
            })
        return resultados

