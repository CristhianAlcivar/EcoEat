from fastapi import APIRouter, HTTPException
from uuid import UUID

from pydantic import BaseModel, constr

from app.application.use_cases.registrar_usuario import RegistrarUsuarioUseCase, TelefonoYaRegistrado
from app.application.use_cases.obtener_imagenes_por_usuario import ObtenerImagenesPorUsuarioUseCase
from app.data.repositories.user_repository_impl import SQLAlchemyUserRepository
from app.data.repositories.image_repository_impl import SQLAlchemyImageRepository

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

class UsuarioRegistro(BaseModel):
    telefono: constr(strip_whitespace=True, min_length=1) # type: ignore
    
@router.post("/")
def registrar_usuario(data: UsuarioRegistro):
    repo = SQLAlchemyUserRepository()
    use_case = RegistrarUsuarioUseCase(repo)
    try:
        user = use_case.execute(telefono=data.telefono)
    except TelefonoYaRegistrado:
        raise HTTPException(status_code=400, detail="El teléfono ya está registrado.")
    return {"msg": "Usuario registrado", "user_id": str(user.id)}

@router.get("/{user_id}/imagenes")
def obtener_imagenes_usuario(user_id: UUID):
    repo = SQLAlchemyImageRepository()
    use_case = ObtenerImagenesPorUsuarioUseCase(repo)
    imagenes = use_case.execute(user_id)
    return [image.__dict__ for image in imagenes]
