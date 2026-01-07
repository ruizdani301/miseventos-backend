from abc import ABC, abstractmethod

from uuid import UUID

from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import UserResponse, UserRequest, UserEmailRequest, UserEmailResponse


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: UserRequest)-> UserResponse:
        pass

    @abstractmethod
    def get_user_by_email(self, useremail: UserEmailRequest)-> UserEmailResponse | None:
        pass
    