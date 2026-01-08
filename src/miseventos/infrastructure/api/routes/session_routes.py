from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from miseventos.infrastructure.persistence.postgresql.implement.session_implement import (
    SessionImplement,
)
from miseventos.use_case.session_usecase import SessionUseCase
from miseventos.infrastructure.api.controllers.session_controller import (
    create_session_controller,
    get_sessions_by_event_id_controller,
    delete_session_controller,
    update_session_controller,
)
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import (
    SessionRequest,
)
from uuid import UUID


def register_sessioncase(db: Session = Depends(get_db)):
    repo = SessionImplement(db)
    return SessionUseCase(repo)


session_router = APIRouter()


@session_router.post("/session/")
async def register_session(
    body: SessionRequest, usecase: SessionUseCase = Depends(register_sessioncase)
):
    response = create_session_controller(usecase)
    print("en controller session")
    print(response.__dict__)
    return await response(body)


@session_router.get("/session/{event_id}")
async def get_sessions_by_event_id(
    event_id: UUID, usecase: SessionUseCase = Depends(register_sessioncase)
):
    response = get_sessions_by_event_id_controller(usecase)
    return await response(event_id)


@session_router.delete("/session/{session_id}")
async def delete_session(
    session_id: UUID, usecase: SessionUseCase = Depends(register_sessioncase)
):
    response = delete_session_controller(usecase)
    return await response(session_id)

    # @session_router.put("/session/")
    # async def update_session(body: SessionRequest, usecase: SessionUseCase = Depends(register_sessioncase)):
    #     response = update_session_controller(usecase)
    return await response(body)
