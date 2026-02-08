from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from miseventos.infrastructure.api.controllers.session_controller import (
    create_session_controller,
    delete_session_controller,
    get_sessions_by_event_id_controller,
    get_sessions_controller,
    update_session_controller,
)
from miseventos.infrastructure.persistence.postgresql.implement.session_implement import (
    SessionImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import (
    SessionRequest,
    SessionUpdateRequest,
)
from miseventos.use_case.session_usecase import SessionUseCase
from token_jwt.jwt_handler import get_current_user


def register_sessioncase(db: Session = Depends(get_db)):
    repo = SessionImplement(db)
    return SessionUseCase(repo)


session_router = APIRouter(tags=["Sesiones"])


@session_router.post("/session/")
async def register_session(
    body: SessionRequest,
    usecase: SessionUseCase = Depends(register_sessioncase),
    current_user: dict = Depends(get_current_user),
):
    """Registra una nueva sesión en un evento."""
    response = create_session_controller(usecase)
    return await response(body)


@session_router.get("/session/{event_id}")
async def get_sessions_by_event_id(
    event_id: UUID,
    usecase: SessionUseCase = Depends(register_sessioncase),
    current_user: dict = Depends(get_current_user),
):
    """
    Get all the session from each session by even_id.
    - **Return**
    ```json
        {
    "success": true,
    "error_message": null,
    "session": [
        {
        "id": "6188cd6e-7f44-445f-901b-211a524a785d",
        "title": "como pasar de ser un cantante a un ingeniero",
        "description": "Es la grandiosa oportunidad de conocer como billy jean dejo ala chica embarazada",
        "created_at": "2026-02-07T23:47:08.346879",
        "event_id": "04d7a0c0-c8ce-4d0e-b8f1-0c7d8bd28952",
        "capacity": 25,
        "time_slot_id": "4b3ab660-3d9a-4bb1-90dd-d202a80d7a73"
        }
    ]
    }
    """
    response = get_sessions_by_event_id_controller(usecase)
    return await response(event_id)


@session_router.delete("/session/{session_id}")
async def delete_session(
    session_id: UUID,
    usecase: SessionUseCase = Depends(register_sessioncase),
    current_user: dict = Depends(get_current_user),
):
    """Elimina una sesión por su ID."""
    response = delete_session_controller(usecase)
    return await response(session_id)


@session_router.put("/session/")
async def update_session(
    body: SessionUpdateRequest,
    usecase: SessionUseCase = Depends(register_sessioncase),
    _current_user: dict = Depends(get_current_user),
):
    """
        Update session 
        - **Return**
        ```json
        {
    "success": true,
    "error_message": null,
    "session": {
        "id": "6188cd6e-7f44-445f-901b-211a524a785d",
        "title": "como pasar de ser un cantante a un ingeniero",
        "description": "Es la grandiosa oportunidad de conocer como billy jean dejo ala chica embarazada",
        "created_at": "2026-02-07T23:47:08.346879",
        "event_id": "04d7a0c0-c8ce-4d0e-b8f1-0c7d8bd28952",
        "capacity": 50,
        "time_slot_id": "4b3ab660-3d9a-4bb1-90dd-d202a80d7a73"
    }
    }
    """
    response = update_session_controller(usecase)
    return await response(body)


@session_router.get("/session/")
async def get_sessions(
    usecase: SessionUseCase = Depends(register_sessioncase),
    _current_user: dict = Depends(get_current_user),
):
    """
    Get  list of all sessions
    - **Return**
    ```json
    {
    "success": true,
    "error_message": null,
    "session": [
            {
            "id": "6188cd6e-7f44-445f-901b-211a524a785d",
            "title": "como pasar de ser un cantante a un ingeniero",
            "description": "Es la grandiosa oportunidad de conocer como billy jean dejo ala chica embarazada",
            "created_at": "2026-02-07T23:47:08.346879",
            "event_id": "04d7a0c0-c8ce-4d0e-b8f1-0c7d8bd28952",
            "capacity": 25,
            "speaker_id": "0a6c9e99-6587-4fd3-9c0f-1d93836228c2",
            "time_slot_id": "4b3ab660-3d9a-4bb1-90dd-d202a80d7a73"
            }
        ]
    }
    """
    response = get_sessions_controller(usecase)
    return await response()
