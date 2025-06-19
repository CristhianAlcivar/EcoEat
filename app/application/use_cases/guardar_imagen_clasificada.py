from app.domain.entities.image import Image
from app.domain.repositories.image_repository import ImageRepository
from uuid import uuid4
from datetime import datetime
from typing import Dict

class GuardarImagenClasificadaUseCase:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, data: Dict):
        image = Image(
            id=uuid4(),
            nombre_imagen=data["nombre_imagen"],
            ruta=data["ruta"],
            usuario_id=data["usuario_id"],
            fecha=data.get("fecha", datetime.utcnow()),
            modelo_id=data["modelo_id"]  
        )
        self.image_repository.save(image)

