"""Session registration use case module.

This module contains the SessionRegisterUseCase class which handles business logic
for registering users to event sessions and managing those registrations.
"""

# Standard library imports
from typing import List
from uuid import UUID

# Local application imports
from miseventos.entitis.sessions import SessionEntity
from miseventos.infrastructure.persistence.postgresql.implement.session_register_implement import (
    SessionRegisterImplement,
)
from miseventos.infrastructure.persistence.postgresql.schemas.session_register_schema import (
    SessionDeleteResponse,
    SessionRegisterDeleteRequest,
    SessionRegisterRequest,
    SessionRegisterResponse,
    registerResponse,
)
from miseventos.repositories.session_repository import SessionRepository


class SessionRegisterUseCase:
    """Use case class for session registration operations.
    
    This class handles the business logic for registering users to event sessions,
    including validation of event/session relationships and managing registration
    lifecycle.
    
    Attributes:
        session_implement: Repository implementation for session registration data access.
    """

    def __init__(self, session_implement: SessionRegisterImplement):
        """Initialize the SessionRegisterUseCase.
        
        Args:
            session_implement: The session registration repository implementation instance.
        """
        self.session_implement = session_implement

    def add_session_register(
        self, session: SessionRegisterRequest
    ) -> registerResponse:
        """Register a user to an event session.
        
        Creates both event-level and session-level registrations. Validates that:
        - User, event, and session exist
        - Session belongs to the specified event
        - User is not already registered for the session
        
        Args:
            session: Registration request containing user_id, event_id, and session_id.
        
        Returns:
            SessionRegisterResponse with success status and registration details
            or error message if registration fails.
        """
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
        """Remove a user's registration from a session.
        
        Validates that the registration exists and belongs to the requesting user
        before deletion.
        
        Args:
            body: Delete request containing registration ID and user ID.
        
        Returns:
            SessionDeleteResponse with success status and deleted registration ID
            or error message if deletion fails.
        """
        session_deleted_response = self.session_implement.delete_session_register(body)
        return session_deleted_response
