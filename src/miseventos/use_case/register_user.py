from miseventos.repositories.user_repository import UserRepository
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import (
    UserImplement,
)
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    UserRequest,
    UserResponse,
    UserEmailResponse,
    UserEmailRequest,
    LoginRequest,
    LoginResponse,
    LoginTokenResponse
)
from miseventos.entitis.user import UserEntity
from utils.cryp_password import encrypt_password, verify_password
from token_jwt.jwt_handler import create_access_token

class UserUseCase:
    def __init__(self, user_implement: UserImplement):
        self.user_implement = user_implement

    def save_user(self, request: UserRequest) -> UserResponse:
        # Check if user with the same email already exists
        existing_user = self.user_implement.get_user_by_email(request.email)
        if existing_user:
            return UserResponse(
                success=False, error_message="User with this email already exists."
            )

        # Create new user
        new_user = UserEntity(email=request.email, password=request.password)

        if not new_user.valid_password():
            return UserResponse(
                id=new_user.id, success=False, error_message="Invalid password format."
            )
        
        new_user.password = encrypt_password(new_user.password)
        

        # Save user to repository
        self.user_implement.add_user(new_user)

        return UserResponse(success=True, user=new_user)

    def find_user_by_email(self, email: UserEmailRequest) -> UserEmailResponse:
        user = self.user_implement.get_user_by_email(email.email)
        if not user:
            return UserEmailResponse(success=False, error_message="User not found.")
        return UserEmailResponse(success=True, email=user.email, id=user.id)

    def login(self, request: LoginRequest) -> LoginTokenResponse:
        user = self.user_implement.get_user_by_email(request.email)
        if not user:
            return LoginTokenResponse(
                success=False, error_message="User not found."
            )
        
        if not verify_password(request.password, user.password):
            return LoginTokenResponse(
                success=False, error_message="Invalid password."
            )
        
        access_token = create_access_token(data={"sub": user.email, "user_id": str(user.id), "role": user.role})
        
        return LoginTokenResponse(
            success=True,
            error_message=None,
            user_id=user.id,
            email=user.email,
            role=user.role,
            access_token=access_token,
        )
