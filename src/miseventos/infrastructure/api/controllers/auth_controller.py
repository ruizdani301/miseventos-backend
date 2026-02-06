from fastapi import HTTPException
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    LoginRequest,
    LoginResponse,
)
from miseventos.use_case.register_user import UserUseCase


def login_controller(usecase: UserUseCase):
    async def controller(body: LoginRequest) -> LoginResponse:
        response = usecase.login(body)
        if not response.success:
            raise HTTPException(status_code=401, detail=response.error_message)
        return response

    return controller
