from miseventos.use_case.session_usecase import SessionUseCase
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import (
    SessionRequest,
    SessionResponse,
    SessionDeleteResponse,
)
from fastapi import HTTPException
from uuid import UUID


def create_session_controller(usecase: SessionUseCase):
    async def controller(request: SessionRequest) -> SessionResponse:
        response = usecase.add_session(request)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def get_sessions_by_event_id_controller(usecase: SessionUseCase):
    async def controller(event_id: UUID) -> SessionResponse:
        response = usecase.get_sessions_by_event_id(event_id)
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error_message)
        return response

    return controller


def delete_session_controller(usecase: SessionUseCase):
    async def controller(session_id: UUID) -> SessionDeleteResponse:
        response = usecase.delete_session(session_id)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def update_session_controller(usecase: SessionUseCase):
    async def controller(request: SessionRequest) -> SessionResponse:
        response = usecase.update_session(request)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller
