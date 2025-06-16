from app.domain.entities.image import Image
from app.domain.repositories.image_repository import ImageRepository
from uuid import UUID
from datetime import datetime
from typing import Dict

class GuardarImagenClasificadaUseCase:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, data: Dict):
        image = Image(
            id=data["id"],
            nombre_imagen=data["nombre_imagen"],
            ruta=data["ruta"],
            usuario_id=data["usuario_id"],
            fecha=data.get("fecha", datetime.utcnow()),
            resultado_modelo=data["resultado_modelo"],
            materiales_renovables=data["materiales_renovables"],
            materiales_no_renovables=data["materiales_no_renovables"],
            confianza_promedio=data["confianza_promedio"]
        )
        self.image_repository.save(image)
