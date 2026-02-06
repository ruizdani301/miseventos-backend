from abc import ABC, abstractmethod
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.session_register_schema import (
    SessionRegisterRequest,
    registerResponse,
    SessionDeleteResponse,
)


class SessionRegisterRepository(ABC):
    @abstractmethod
    def add_session_register(self, session: SessionRegisterRequest) -> registerResponse:
        pass

    @abstractmethod
    def delete_session_register(
        self, body: SessionRegisterRequest
    ) -> SessionDeleteResponse:
        pass
