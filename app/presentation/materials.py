from fastapi import APIRouter

from app.data.repositories.material_repository_impl import SQLAlchemyMaterialRepository
from app.data.db.database import SessionLocal

router = APIRouter(prefix="/materiales", tags=["materiales"])

@router.get("/")
def listar_todas_materiales():
    with SessionLocal() as session:
        repo = SQLAlchemyMaterialRepository(session)
        return repo.list_all()