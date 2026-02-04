from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from miseventos.infrastructure.persistence.postgresql.implement.session_register_implement import (
    SessionRegisterImplement,
)
from miseventos.use_case.session_register_usecase import SessionRegisterUseCase
from miseventos.infrastructure.api.controllers.session_register_controller import (
    create_register_session_controller,
    delete_register_session_controller

)
from token_jwt.jwt_handler import get_current_user
from miseventos.infrastructure.persistence.postgresql.schemas.session_register_schema import (
    SessionRegisterRequest,
    SessionRegisterDeleteRequest
)
from uuid import UUID
from fastapi import Request, HTTPException

from fastapi import Request


def register_sessioncase(db: Session = Depends(get_db)):
    repo = SessionRegisterImplement(db)
    return SessionRegisterUseCase(repo)


session_register_router = APIRouter(tags=["Registrar Sesiones"])


@session_register_router.post("/register-session/")
async def register_session(
    body: SessionRegisterRequest,
    usecase: SessionRegisterUseCase = Depends(register_sessioncase),
    current_user: dict = Depends(get_current_user)
):
    """Registra una nueva sesión en un evento."""

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
    current_user: dict = Depends(get_current_user)
):
    """Elimina el registro de una sesión."""
    payload = SessionRegisterDeleteRequest(
       register_id=register_id,
       user_id=current_user["user_id"]
    )
    response = delete_register_session_controller(usecase)
    return await response(payload)
