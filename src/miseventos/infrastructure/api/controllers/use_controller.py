from fastapi import HTTPException
from ....infrastructure.persistence.postgresql.schemas.user_schema import (
    UserRequest,
    UserResponse,
    UserEmailRequest,
    UserEmailResponse,
)
from miseventos.use_case.register_user import UserUseCase


def add_user_controller(usecase: UserUseCase):
    async def controller(body: UserRequest) -> UserResponse:

        response = usecase.save_user(body)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def find_by_email_controller(usecase: UserUseCase):
    async def controller(body: UserEmailRequest) -> UserEmailResponse:
        response = usecase.find_user_by_email(body)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller
