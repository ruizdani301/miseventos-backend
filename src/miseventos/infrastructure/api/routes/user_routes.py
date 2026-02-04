from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from ....use_case.register_user import UserUseCase
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import (
    UserImplement,
)
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    UserRequest,
    UserEmailRequest,
)
from miseventos.infrastructure.api.controllers.use_controller import (
    add_user_controller,
    find_by_email_controller,
)


def register_usecase(db: Session = Depends(get_db)):
    repo = UserImplement(
        db
    )  
    return UserUseCase(repo)  

user_router = APIRouter(tags=["Usuarios"])


@user_router.post("/user/register")
async def register_user(
    body: UserRequest, usecase: UserUseCase = Depends(register_usecase)
):
    """Registra un nuevo usuario en el sistema."""
    response = add_user_controller(usecase)

    return await response(body)


@user_router.get("/user/{email}")
async def get_user_by_email(
    email: str, usecase: UserUseCase = Depends(register_usecase)
):
    """Busca un usuario por su dirección de correo electrónico."""
    response = find_by_email_controller(usecase)
    return await response(email)
