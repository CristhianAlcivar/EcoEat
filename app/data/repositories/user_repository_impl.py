from datetime import datetime, timezone
from typing import List
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.data.db.models import UserModel
from uuid import UUID, uuid4

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, user_id):
        user_model = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None
        return User(id=user_model.id, telefono=user_model.telefono, registro=user_model.registro)

    def get_by_telefono(self, telefono):
        user_model = self.session.query(UserModel).filter(UserModel.telefono == telefono).first()
        if not user_model:
            return None
        return User(id=user_model.id, telefono=user_model.telefono, registro=user_model.registro)

    def save(self, user: User) -> None:
        # Solo crear valores por defecto si vienen vacíos
        if not user.id:
            user.id = uuid4()
        if not user.registro:
            user.registro = datetime.now(timezone.utc)

        user_model = UserModel(
            id=user.id,
            telefono=user.telefono,
            registro=user.registro
        )
        self.session.add(user_model)
        self.session.commit()
    
    def list_all(self) -> List[User]:
        users = self.session.query(UserModel).all()
        return [
            User(id=user.id, telefono=user.telefono, registro=user.registro)
            for user in users
        ]
