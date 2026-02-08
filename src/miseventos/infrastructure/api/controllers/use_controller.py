from typing import List
from uuid import UUID

from fastapi import HTTPException

from miseventos.entitis.user import UserEntity
from miseventos.use_case.register_user import UserUseCase

from ....infrastructure.persistence.postgresql.schemas.user_schema import (
    UserEmailRequest,
    UserEmailResponse,
    UserRequest,
    UserResponse,
)


def add_user_controller(usecase: UserUseCase):
    async def controller(body: UserRequest) -> UserResponse:

        response = usecase.save_user(body)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def update_user_controller(usecase: UserUseCase):
    async def controller(body: UserRequest) -> UserResponse:
        response = usecase.update_user(body)
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


def find_all_users_controller(usecase: UserUseCase):
    async def controller() -> List[UserEntity]:
        response = usecase.find_all_users()
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def delete_user_controller(usecase: UserUseCase):
    async def controller(id: UUID) -> UserResponse:
        response = usecase.delete_user(id)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller
