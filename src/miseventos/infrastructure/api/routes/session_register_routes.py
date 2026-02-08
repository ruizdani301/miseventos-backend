from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from miseventos.infrastructure.api.controllers.session_register_controller import (
    create_register_session_controller,
    delete_register_session_controller,
)
from miseventos.infrastructure.persistence.postgresql.implement.session_register_implement import (
    SessionRegisterImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from miseventos.infrastructure.persistence.postgresql.schemas.session_register_schema import (
    SessionRegisterDeleteRequest,
    SessionRegisterRequest,
)
from miseventos.use_case.session_register_usecase import SessionRegisterUseCase
from token_jwt.jwt_handler import get_current_user


def register_sessioncase(db: Session = Depends(get_db)):
    repo = SessionRegisterImplement(db)
    return SessionRegisterUseCase(repo)


session_register_router = APIRouter(tags=["Registrar Sesiones"])


@session_register_router.post("/register-session/")
async def register_session(
    body: SessionRegisterRequest,
    usecase: SessionRegisterUseCase = Depends(register_sessioncase),
    current_user: dict = Depends(get_current_user),
):
    """
    Register a new session in an event.

    Args:
        body (SessionRegisterRequest): Request containing event_id, user_id, and session_id.
        usecase (SessionRegisterUseCase): Use case to register the session.
        current_user (dict): Current user.
        ```json
        **Returns**
        {
            "success": true,
            "message": "Session registered successfully",
            "session_detail": {
                "event_registration_id": "2563jhhbs98830djjd0h",
                "id": "2563jhhbs98830djjd0h",
                "number_registered": 1,
                "event_id": "2563jhhbs98830djjd0h",
                "session_id": "2563jhhbs98830djjd0h",
                "message": "Registro Exitoso",
            }
        }
       '''
    """

    payload = SessionRegisterRequest(
        event_id=body.event_id,
        user_id=current_user["user_id"],
        session_id=body.session_id,
    )

    response = create_register_session_controller(usecase)
    return await response(payload)


@session_register_router.delete("/register-session/{register_id}/")
async def delete_register_session(
    register_id: UUID,
    usecase: SessionRegisterUseCase = Depends(register_sessioncase),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete the record of a session.

    Args:
        register_id (UUID): ID of the record to delete.
        usecase (SessionRegisterUseCase): Use case to delete the registration.
        current_user (dict): Current user.
        ```json
        **Returns**
        {
            "success": true,
            "message": "Record deleted successfully",
            "id": "2563jhhbs98830djjd0h
        }
        '''
    """
    payload = SessionRegisterDeleteRequest(
        register_id=register_id, user_id=current_user["user_id"]
    )
    response = delete_register_session_controller(usecase)
    return await response(payload)
