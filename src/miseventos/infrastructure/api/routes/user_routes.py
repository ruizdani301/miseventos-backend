from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from ....use_case.register_user import UserUseCase
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import (
    UserImplement,
)
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    UserRequest,
    UserEmailRequest,
    UserUpdateRequest,
)
from miseventos.infrastructure.api.controllers.use_controller import (
    add_user_controller,
    find_by_email_controller,
    update_user_controller,
    find_all_users_controller,
    delete_user_controller)


def register_usecase(db: Session = Depends(get_db)):
    repo = UserImplement(db)  
    return UserUseCase(repo)  

user_router = APIRouter(tags=["Usuarios"])


@user_router.post("/user/register")
async def register_user(
    body: UserRequest, usecase: UserUseCase = Depends(register_usecase)
):
    """Registra un nuevo usuario en el sistema."""
    response = add_user_controller(usecase)

    return await response(body)


@user_router.put("/user/")
async def update_user(
    body: UserUpdateRequest, usecase: UserUseCase = Depends(register_usecase)
):
    """Actualiza un usuario por su dirección de correo electrónico."""
    print("ACTUALIZAR USUARIO ROUTER")
    print(body)
    response = update_user_controller(usecase)
    return await response(body)

@user_router.get("/user/{email}")
async def get_user_by_email(
    email: str, usecase: UserUseCase = Depends(register_usecase)
):
    """Busca un usuario por su dirección de correo electrónico."""
    response = find_by_email_controller(usecase)
    return await response(email)

@user_router.get("/user/")
async def get_all_users(
    usecase: UserUseCase = Depends(register_usecase)
):
    """Busca todos los usuarios."""
    response = find_all_users_controller(usecase)
    return await response()

@user_router.delete("/user/{id}")
async def delete_user(
    id: UUID, usecase: UserUseCase = Depends(register_usecase)
):
    """Elimina un usuario por su ID."""
    response = delete_user_controller(usecase)
    return await response(id)
