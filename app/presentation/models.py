from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.data.repositories.model_repository_impl import SQLAlchemyModelRepository
from app.data.db.database import SessionLocal
from uuid import UUID

router = APIRouter(prefix="/modelos", tags=["modelos"])

class Models(BaseModel):
    id: Optional[UUID] = None
    nombre: str
    formato: str
    score: float
    precision: float
    recall: float
    dataset: str
    fecha_entrenamiento: datetime
    optimizado: bool
    
@router.get("/")
def listar_todos_modelos():
    with SessionLocal() as session:
        repo = SQLAlchemyModelRepository(session)
        return repo.list_all()

@router.get("/{model_id}")
def obtener_modelo(model_id: UUID):
    with SessionLocal() as session:
        repo = SQLAlchemyModelRepository(session)
        modelo = repo.get_by_id(model_id)
        if not modelo:
            raise HTTPException(status_code=404, detail="Modelo no encontrado")
        return modelo

@router.post("/")
def crear_modelo(modelo: Models):
    with SessionLocal() as session:
        repo = SQLAlchemyModelRepository(session)
        return repo.save(modelo)

@router.put("/{model_id}")
def actualizar_modelo(model_id: UUID, modelo: Models):
    with SessionLocal() as session:
        repo = SQLAlchemyModelRepository(session)
        
        updated_data = modelo.dict(exclude_unset=True)
        actualizado = repo.update(model_id, updated_data)
        
        if not actualizado:
            raise HTTPException(status_code=404, detail="Modelo no encontrado")
        return actualizado


@router.delete("/{model_id}")
def eliminar_modelo(model_id: UUID):
    with SessionLocal() as session:
        repo = SQLAlchemyModelRepository(session)
        exito = repo.delete(model_id)
        if not exito:
            raise HTTPException(status_code=404, detail="Modelo no encontrado")
        return {"ok": True}
