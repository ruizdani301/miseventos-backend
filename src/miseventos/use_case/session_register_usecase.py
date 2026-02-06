from miseventos.repositories.session_repository import SessionRepository
from miseventos.entitis.sessions import SessionEntity
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.implement.session_register_implement import (
    SessionRegisterImplement,
)
from typing import List
from miseventos.infrastructure.persistence.postgresql.schemas.session_register_schema import (
    SessionRegisterResponse,
    SessionDeleteResponse,
    SessionRegisterRequest,
    registerResponse,
    SessionRegisterDeleteRequest,
)


class SessionRegisterUseCase:
    def __init__(self, session_implement: SessionRegisterImplement):
        self.session_implement = session_implement

    def add_session_register(self, session: SessionRegisterRequest) -> registerResponse:
        new_register = self.session_implement.add_session_register(session)
        if not new_register:
            return SessionRegisterResponse(
                success=False, error_message="Error saving register."
            )
        if not new_register.success:
            return SessionRegisterResponse(
                success=False, error_message=new_register.error_message
            )

        return SessionRegisterResponse(
            success=True, error_message=None, session_detail=new_register
        )

    def delete_session_register(
        self, body: SessionRegisterDeleteRequest
    ) -> SessionDeleteResponse:
        session_deleted_response = self.session_implement.delete_session_register(body)
        return session_deleted_response
