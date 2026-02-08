"""Session management use case module.

This module contains the SessionUseCase class which handles business logic
for managing event sessions including CRUD operations.
"""

# Standard library imports
from typing import List
from uuid import UUID

# Local application imports
from miseventos.entitis.sessions import SessionEntity
from miseventos.infrastructure.persistence.postgresql.implement.session_implement import (
    SessionImplement,
)
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import (
    SessionDeleteResponse,
    SessionRequest,
    SessionResponse,
    SessionSpeakerResponse,
    SessionUpdateRequest,
)
from miseventos.repositories.session_repository import SessionRepository


class SessionUseCase:
    """Use case class for session management operations.
    
    This class encapsulates all business logic related to event sessions,
    including CRUD operations and event-session relationships.
    
    Attributes:
        session_implement: Repository implementation for session data access.
    """

    def __init__(self, session_implement: SessionImplement):
        """Initialize the SessionUseCase.
        
        Args:
            session_implement: The session repository implementation instance.
        """
        self.session_implement = session_implement

    def get_sessions_by_event_id(self, event_id: UUID) -> SessionResponse | None:
        """Retrieve all sessions for a specific event.
        
        Args:
            event_id: UUID of the event to fetch sessions for.
        
        Returns:
            SessionResponse containing list of sessions or error message if
            no sessions found for the event.
        """
        data_session = self.session_implement.get_session_by_event_id(event_id)
        if not data_session:
            return SessionResponse(
                success=False, error_message="No sessions found for the given event ID."
            )
        return SessionResponse(success=True, error_message=None, session=data_session)

    def add_session(self, session: SessionRequest) -> SessionResponse:
        """Create a new session for an event.
        
        Args:
            session: Session creation request containing title, description,
                event_id, time_slot_id, and other session details.
        
        Returns:
            SessionResponse with success status and created session or error message.
        """
        new_session = self.session_implement.add_session(session)
        if not new_session:
            return SessionResponse(success=False, error_message="Error saving session.")
        return SessionResponse(success=True, error_message=None, session=new_session)

    def delete_session(self, session_id: UUID) -> SessionDeleteResponse:
        """Delete a session by ID.
        
        Args:
            session_id: UUID of the session to delete.
        
        Returns:
            SessionDeleteResponse with success status and deleted session ID
            or error message.
        """
        deleted_id = self.session_implement.delete_session(session_id)
        if not deleted_id:
            return SessionDeleteResponse(
                success=False, error_message="Error deleting session."
            )
        return SessionDeleteResponse(id=deleted_id, success=True, error_message=None)

    def update_session(self, session: SessionUpdateRequest) -> SessionResponse:
        """Update an existing session.
        
        Args:
            session: Session update request containing session ID and updated fields.
        
        Returns:
            SessionResponse with success status and updated session or error message.
        """
        updated_session = self.session_implement.update_session(session)
        if not updated_session:
            return SessionResponse(
                success=False, error_message="Error updating session."
            )
        return SessionResponse(
            success=True, error_message=None, session=updated_session
        )

    def get_sessions(self) -> SessionSpeakerResponse | None:
        """Retrieve all sessions in the system.
        
        Returns:
            SessionSpeakerResponse containing list of all sessions or error message
            if no sessions found.
        """
        data_session = self.session_implement.get_sessions()
        if not data_session:
            return SessionSpeakerResponse(success=False, error_message="No sessions found.")
        return SessionSpeakerResponse(success=True, error_message=None, session=data_session)
