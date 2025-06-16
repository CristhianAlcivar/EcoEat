from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.data.db.models import UserModel
from app.data.db.database import SessionLocal
from uuid import UUID

class SQLAlchemyUserRepository(UserRepository):
    def get_by_id(self, user_id: UUID) -> User:
        with SessionLocal() as session:
            user_model = session.query(UserModel).filter(UserModel.id == user_id).first()
            if not user_model:
                return None
            return User(id=user_model.id, telefono=user_model.telefono, registro=user_model.registro)
        
    def get_by_telefono(self, telefono: UUID) -> User:
        with SessionLocal() as session:
            user_model = session.query(UserModel).filter(UserModel.telefono == telefono).first()
            if not user_model:
                return None
            return User(id=user_model.id, telefono=user_model.telefono, registro=user_model.registro)

    def save(self, user: User) -> None:
        with SessionLocal() as session:
            user_model = UserModel(id=user.id, telefono=user.telefono, registro=user.registro)
            session.add(user_model)
