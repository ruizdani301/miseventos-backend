from miseventos.repositories.user_repository import UserRepository
from miseventos.entitis.user import UserEntity
from sqlalchemy import orm
from miseventos.infrastructure.persistence.postgresql.models.user_model import (
    User as userModel,
)
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName


class UserImplement(UserRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def add_user(self, user: UserEntity) -> UserEntity:
        role = user.role if user.role else RoleName.ASSISTANT.value
        new_user_model = userModel(
            password_hash=user.password, email=user.email, role=role
        )
        self.session.add(new_user_model)
        self.session.commit()
        self.session.refresh(new_user_model)
        return UserEntity(id=new_user_model.id, email=new_user_model.email)

    def get_user_by_email(self, useremail: str) -> UserEntity | None:
        user_model = self.session.query(userModel).filter_by(email=useremail).first()
        if user_model:
            return UserEntity(id=user_model.id, email=user_model.email)
        return None
