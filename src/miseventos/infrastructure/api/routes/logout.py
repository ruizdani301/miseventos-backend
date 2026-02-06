from fastapi import APIRouter, Depends, Response, HTTPException
from typing import Optional
# Asegúrate de importar HTTPException
from token_jwt.jwt_handler import get_current_user

logout_router = APIRouter(
    tags=["Authentication"],
    responses={
        401: {"description": "No autenticado"},
        200: {"description": "Logout exitoso"}
    }
)

@logout_router.post("/logout")
async def logout(
    response: Response, 
    current_user: dict = Depends(get_current_user) 
):
    """
    Cierra sesión del usuario eliminando la cookie HttpOnly.
    """
    
    if not current_user:
        raise HTTPException(status_code=401, detail="No autorizado")
        
    response.delete_cookie(
        key="auth_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=False  
    )
    
    return {
        "success": True,
        "message": f"Sesión cerrada para {current_user.get('email')}"
    }