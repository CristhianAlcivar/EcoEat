from app.domain.entities.material import Material
from app.domain.repositories.material_repository import MaterialRepository
from app.data.db.models import MaterialModel

class SQLAlchemyMaterialRepository(MaterialRepository):
    def __init__(self, session):
        self.session = session

    def list_all(self) -> list[Material]:
        records = self.session.query(MaterialModel).all()
        return [
            Material(
                id=str(r.material_id),
                nombre_material=r.nombre_material,
                tipo_material=r.tipo_material,
                renovable=r.renovable,
                reciclable=r.reciclable,
                impacto_ambiental=r.impacto_ambiental,
                imagen_url=r.imagen_url
            )
            for r in records
        ]

    def get_by_id(self, material_id: str) -> Material:
        r = self.session.query(MaterialModel).filter(MaterialModel.material_id == material_id).first()
        if not r:
            return None
        return Material(
            id=str(r.material_id),
            nombre_material=r.nombre_material,
            tipo_material=r.tipo_material,
            renovable=r.renovable,
            reciclable=r.reciclable,
            impacto_ambiental=r.impacto_ambiental,
            imagen_url=r.imagen_url
        )
