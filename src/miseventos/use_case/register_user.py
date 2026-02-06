from miseventos.repositories.user_repository import UserRepository
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import (
    UserImplement,
)
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    UserRequest,
    UserResponse,
    UserEmailResponse,
    UserEmailRequest,
    LoginRequest,
    LoginResponse,
    LoginTokenResponse,
    UserUpdateResponse,
    UserUpdateRequest,
    UserListResponse
)
from miseventos.entitis.user import UserEntity
from utils.cryp_password import encrypt_password, verify_password
from token_jwt.jwt_handler import create_access_token

class UserUseCase:
    def __init__(self, user_implement: UserImplement):
        self.user_implement = user_implement

    def save_user(self, request: UserRequest) -> UserResponse:
        existing_user = self.user_implement.get_user_by_email(request.email)
        if existing_user:
            return UserResponse(
                success=False, error_message="User with this email already exists."
            )
        new_user = UserEntity(email=request.email, password=request.password, role=request.role or "assistant")

        if not new_user.valid_password():
            return UserResponse(
                id=new_user.id, success=False, error_message="Invalid password format."
            )
        new_user.password = encrypt_password(new_user.password)
        
        response = self.user_implement.add_user(new_user)
        if not response:
            return UserResponse(
                success=False, error_message="User not found.", id=None
            )
        return UserResponse(success=True, error_message=None, id=response.id)

    def find_all_users(self) -> UserListResponse:
        response = self.user_implement.get_users()
        if not response:
            return UserListResponse(
                success=False, error_message="User not found.", users=None
            )
        return UserListResponse(success=True, error_message=None, users=response)

    def update_user(self, request: UserUpdateRequest) -> UserUpdateResponse:
        existing_user = self.user_implement.get_user_by_id(request.id)
        if not existing_user:
            return UserUpdateResponse(
                success=False, error_message="User not found."
            )
        
        if request.password:
            if request.password == existing_user.password:
                password_to_save = existing_user.password
            
            elif verify_password(request.password, existing_user.password):
                password_to_save = existing_user.password
            else:
                password_to_save = encrypt_password(request.password)
        
        new_user = UserEntity(
            id=request.id,
            email=request.email,
            password=password_to_save,
            role=request.role
        )
        response = self.user_implement.update_user(new_user)
        if not response:
            return UserUpdateResponse(
                success=False, error_message="User not found.", user=None
            )

        return UserUpdateResponse(success=True, error_message=None ,user=response)


    def find_user_by_email(self, email: UserEmailRequest) -> UserEmailResponse:
        user = self.user_implement.get_user_by_email(email.email)
        if not user:
            return UserEmailResponse(success=False, error_message="User not found.")
        return UserEmailResponse(success=True, email=user.email, id=user.id)
 
    def delete_user(self, id: UUID) -> UserResponse:
        response = self.user_implement.delete_user(id)
        if not response:
            return UserResponse(
                success=False, error_message="User not found.", id=None
            )
        return UserResponse(success=True, error_message=None, id=response.id)

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
        
        access_token = create_access_token(data={"email": user.email, "user_id": str(user.id), "role": user.role})
        
        return LoginTokenResponse(
            success=True,
            error_message=None,
            user_id=user.id,
            email=user.email,
            role=user.role,
            access_token=access_token,
        )
