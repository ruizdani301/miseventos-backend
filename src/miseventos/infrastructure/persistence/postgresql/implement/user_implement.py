from miseventos.repositories.user_repository import UserRepository
from miseventos.entitis.user import UserEntity
from sqlalchemy import orm
from miseventos.infrastructure.persistence.postgresql.models.user_model import (
    User as userModel,
)
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName
from typing import List


class UserImplement(UserRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def add_user(self, user: UserEntity) -> UserEntity:
        try:
            role = user.role if user.role else RoleName.ASSISTANT.value
            new_user_model = userModel(
                password_hash=user.password, email=user.email, role=role
            )
            self.session.add(new_user_model)
            self.session.commit()
            self.session.refresh(new_user_model)
            return UserEntity(id=new_user_model.id, email=new_user_model.email)
        except Exception as e:
            self.session.rollback()
            raise e

    def get_users(self) -> List[UserEntity]:
        try:
            users_model = self.session.query(userModel).all()
            return [
                UserEntity(
                    id=user.id,
                    email=user.email,
                    password=user.password_hash,
                    role=user.role,
                )
                for user in users_model
            ]
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_user(self, user_id: UUID) -> UserEntity:
        try:
            user_model = self.session.query(userModel).filter_by(id=user_id).first()
            if user_model:
                self.session.delete(user_model)
                self.session.commit()
                return UserEntity(id=user_model.id)
        except Exception as e:
            self.session.rollback()
            raise e

    def update_user(self, user: UserEntity) -> UserEntity | None:
        try:
            user_model = self.session.query(userModel).filter_by(id=user.id).first()
            if user_model:
                user_model.email = user.email
                user_model.password_hash = user.password
                user_model.role = user.role
                self.session.commit()
                return UserEntity(
                    id=user_model.id, email=user_model.email, role=user_model.role
                )
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def get_user_by_id(self, user_id: int) -> UserEntity | None:
        try:
            user_model = self.session.query(userModel).filter_by(id=user_id).first()
            if user_model:
                return UserEntity(
                    id=user_model.id,
                    email=user_model.email,
                    password=user_model.password_hash,
                    role=user_model.role,
                )
            return None
        except Exception as e:
            raise e

    def get_user_by_email(self, useremail: str) -> UserEntity | None:
        try:
            user_model = (
                self.session.query(userModel).filter_by(email=useremail).first()
            )
            if user_model:
                return UserEntity(
                    id=user_model.id,
                    email=user_model.email,
                    password=user_model.password_hash,
                    role=user_model.role,
                )
            return None
        except Exception as e:
            raise e
