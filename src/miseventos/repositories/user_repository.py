from abc import ABC, abstractmethod

from typing import List
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    UserResponse,
    UserRequest,
    UserEmailRequest,
    UserEmailResponse,
)
from miseventos.entitis.user import UserEntity


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: UserRequest) -> UserEntity:
        pass

    @abstractmethod
    def get_user_by_email(self, useremail: UserEmailRequest) -> UserEntity | None:
        pass

    @abstractmethod
    def get_users(self) -> List[UserEntity]:
        pass

    @abstractmethod
    def delete_user(self, user_id: UUID) -> bool:
        pass

    @abstractmethod
    def update_user(self, user: UserEntity) -> UserEntity:
        pass
