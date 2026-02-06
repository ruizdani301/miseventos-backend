from fastapi import APIRouter, Depends, Response
from sqlmodel import Session
from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import UserImplement
from miseventos.use_case.register_user import UserUseCase
from miseventos.infrastructure.api.controllers.auth_controller import login_controller
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import LoginRequest, LoginResponse
from fastapi import Request

def register_auth_case(db: Session = Depends(get_db)):
    repo = UserImplement(db)
    return UserUseCase(repo)

login_router = APIRouter(tags=["Autenticación"])

@login_router.post("/login")
async def login(
    body: LoginRequest, response: Response, usecase: UserUseCase = Depends(register_auth_case)
):
    """Acceso de usuario y generación de token JWT."""
    
    response_controller = login_controller(usecase)
    response_controller = await response_controller(body)
    
    

    if response_controller.success:
        response.set_cookie(
            key="auth_token",           
            value=response_controller.access_token, 
            httponly=True,              
            secure=False,                
            samesite="lax",             
            max_age=24 * 60 * 60,
            path="/",
            domain="127.0.0.1",
        )
        return LoginResponse(
            success=True,
            error_message=None,
            user_id=response_controller.user_id,
            email=response_controller.email,
            role=response_controller.role,
        )
    else:
        return LoginResponse(
            success=False,
            error_message=response_controller.error_message,
            user_id=None,
            email=None,
            role=None,
        )