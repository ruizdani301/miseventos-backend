from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from miseventos.infrastructure.api.controllers.use_controller import (
    add_user_controller,
    delete_user_controller,
    find_all_users_controller,
    find_by_email_controller,
    update_user_controller,
)
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import (
    UserImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    UserRequest,
    UserUpdateRequest,
)
from miseventos.use_case.register_user import UserUseCase
from token_jwt.jwt_handler import get_current_user


def register_usecase(db: Session = Depends(get_db)):
    repo = UserImplement(db)
    return UserUseCase(repo)


user_router = APIRouter(tags=["Usuarios"])


@user_router.post("/user/register")
async def register_user(
    body: UserRequest,
    usecase: UserUseCase = Depends(register_usecase),
):
    """
    Register a new user in the system
    **Args:**
    - body (UserUpdateRequest): User update request.
    - usecase (UserUseCase): Use case responsible for updating the user.
     
    ```json
    Returns:
    {
    success: bool,
    error_message: Optional[str] = None,
    id: UUID
    }
    """
    response = add_user_controller(usecase)

    return await response(body)


@user_router.put("/user/")
async def update_user(
    body: UserUpdateRequest,
    usecase: UserUseCase = Depends(register_usecase),
    current_user: dict = Depends(get_current_user),
):
    """
    Update a user.

    **Args:**
    - body (UserUpdateRequest): User update request.
    - usecase (UserUseCase): Use case responsible for updating the user.
    - current_user (dict): Currently authenticated user.

    **Returns:**
    ```json
    {
    success: bool,
    error_message: Optional[str] = None,
    user:{
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "email": "string",
        "role": "assistant"
        }
    }
    """
    response = update_user_controller(usecase)
    return await response(body)


@user_router.get("/user/{email}")
async def get_user_by_email(
    email: str,
    usecase: UserUseCase = Depends(register_usecase),
    current_user: dict = Depends(get_current_user),
):  
    """
    Search for a user by email address.

    **Args:**
    - email (str): Email of the user to search for.
    - usecase (UserUseCase): Use case responsible for finding the user.
    - current_user (dict): Currently authenticated user.

    **Returns:**
    ```json
    {
    success: bool,
    error_message: Optional[str] = None,
    users: [
    {
      "id": "52db24ad-155e-4621-a132-d8228670c116",
      "email": "ruizdani301@gmail.com",
      "role": "assistant"
    },
    {
      "id": "e6d05330-40bf-41b6-8efa-87f8acff4f06",
      "email": "ruizdani@gmail.com",
      "role": "assistant"
    },
        ]

    }
    """
   
    response = find_by_email_controller(usecase)
    return await response(email)


@user_router.get("/user/")
async def get_all_users(
    usecase: UserUseCase = Depends(register_usecase),
    current_user: dict = Depends(get_current_user),
):
    """
        Retrieve all users.

        **Args:**
        - usecase (UserUseCase): Use case responsible for retrieving all users.
        - current_user (dict): Currently authenticated user.

        **Returns:**
        ```json
        {
        success: bool,
        error_message: Optional[str] = None,
        users: [
            {
            id: UUID,
            email: str,
            name: str,
            role: RoleName,
            created_at: datetime
            }
        ]
        }
    """

    response = find_all_users_controller(usecase)
    return await response()


@user_router.delete("/user/{id}")
async def delete_user(
    id: UUID,
    usecase: UserUseCase = Depends(register_usecase),
    current_user: dict = Depends(get_current_user),
):
    '''
    Elimina un usuario por su ID.

    Args:
        id (UUID): ID del usuario a eliminar.
        usecase (UserUseCase): Caso de uso para eliminar el usuario.
        current_user (dict): Usuario actual.

    Returns:
    {
        id: UUID | None = None
        success: bool
        error_message: Optional[str] = None
    }
    '''
    response = delete_user_controller(usecase)
    return await response(id)
