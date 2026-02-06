from fastapi import APIRouter, Depends
from miseventos.infrastructure.persistence.postgresql.models.user_model import User
from token_jwt.jwt_handler import get_current_user
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    AuthResponse,
    UserAuthResponse,
)
from fastapi import HTTPException

auth_router = APIRouter(tags=["Auth"])


@auth_router.get("/auth/me/")
async def verify_auth(current_user: dict = Depends(get_current_user)):
    """Verifica si el usuario está autenticado."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Usuario no autenticado")

    user_auth = UserAuthResponse(
        id=current_user["user_id"],
        email=current_user["email"],
        role=current_user["role"],
    )
    user = AuthResponse(success=True, error_message=None, user=user_auth)
    return user
