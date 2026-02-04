from fastapi import Depends, Request, Response
from typing import Optional
from fastapi import APIRouter
from token_jwt.jwt_handler import get_current_user

logout_router = APIRouter(

    tags=["Authentication"],  # Para Swagger UI
    responses={
        401: {"description": "No autenticado"},
        200: {"description": "Logout exitoso"}
    }
)

@logout_router.post("/logout")
async def logout(
    response: Response, 
    request: Request,
    #current_user: Optional[dict] = Depends(get_current_user())
):
    """
    Cierra sesión del usuario.
    """
    return "bienvenido al logout"
    # # Permitir que Swagger vea el endpoint aunque no haya usuario
    # # (pero la operación real requerirá autenticación)
    
    # if not current_user:
    #     # Para Swagger/testing, mostrar endpoint pero indicar que requiere auth
    #     pass  # Swagger podrá ver el endpoint
    
    # response.delete_cookie(
    #     key="auth_token",
    #     path="/",
    #     httponly=True,
    #     secure=False  # Cambia a True en producción
    # )
    
    # return {
    #     "success": True,
    #     "message": "Sesión cerrada",
    #     "user": current_user.get("email") if current_user else None
    # }