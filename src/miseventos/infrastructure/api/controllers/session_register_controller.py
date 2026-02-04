from miseventos.use_case.session_usecase import SessionUseCase
from miseventos.infrastructure.persistence.postgresql.schemas.session_register_schema import (
    SessionRegisterRequest,
    SessionRegisterResponse,
    SessionDeleteResponse,
    SessionRegisterDeleteRequest
)
from miseventos.use_case.session_register_usecase import SessionRegisterUseCase
from fastapi import HTTPException
from uuid import UUID


def create_register_session_controller(usecase: SessionRegisterUseCase):
    async def controller(request: SessionRegisterRequest) -> SessionRegisterResponse:
        response = usecase.add_session_register(request)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def delete_register_session_controller(usecase: SessionRegisterUseCase):
    async def controller(body: SessionRegisterDeleteRequest) -> SessionDeleteResponse:
        response = usecase.delete_session_register(body)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller
