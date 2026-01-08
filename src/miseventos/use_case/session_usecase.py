from miseventos.repositories.session_repository import SessionRepository
from miseventos.entitis.sessions import SessionEntity
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.implement.session_implement import (
    SessionImplement,
)
from typing import List
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import (
    SessionResponse,
    SessionDeleteResponse,
)


class SessionUseCase:
    def __init__(self, session_implement: SessionImplement):
        self.session_implement = session_implement

    def get_sessions_by_event_id(self, event_id) -> SessionResponse | None:
        data_session = self.session_implement.get_session_by_event_id(event_id)
        if not data_session:
            return SessionResponse(
                success=False, error_message="No sessions found for the given event ID."
            )
        return SessionResponse(success=True, error_message=None, session=data_session)

    def add_session(self, session: SessionEntity) -> SessionResponse:
        new_session = self.session_implement.add_session(session)
        if not new_session:
            return SessionResponse(success=False, error_message="Error saving session.")
        return SessionResponse(success=True, error_message=None, session=new_session)

    def delete_session(self, session_id: UUID) -> SessionDeleteResponse:
        deleted_id = self.session_implement.delete_session(session_id)
        if not deleted_id:
            return SessionDeleteResponse(
                success=False, error_message="Error deleting session."
            )
        return SessionDeleteResponse(id=deleted_id, success=True, error_message=None)

    def update_session(self, session: SessionEntity) -> SessionResponse:
        updated_session = self.session_implement.update_session(session)
        if not updated_session:
            return SessionResponse(
                success=False, error_message="Error updating session."
            )
        return SessionResponse(
            success=True, error_message=None, session=updated_session
        )
