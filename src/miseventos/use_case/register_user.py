from miseventos.repositories.user_repository import UserRepository
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import UserImplement
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import UserRequest, UserResponse, UserEmailResponse, UserEmailRequest
from miseventos.entitis.user import UserEntity

class UserUseCase:
    def __init__(self, user_implement: UserImplement):
        self.user_implement = user_implement

    def save_user(self, request: UserRequest)->UserResponse:
        # Check if user with the same email already exists
        existing_user = self.user_implement.get_user_by_email(request.email)
        print(existing_user)
        if existing_user:
            return UserResponse(
              
                success=False,
                error_message="User with this email already exists."
            )

        # Create new user
        new_user = UserEntity(
            
            email=request.email,
            password=request.password
        )

   
        if not new_user.valid_password():
            return UserResponse(
                id=new_user.id,
                success=False,
                error_message="Invalid password format."
            )

        # Save user to repository
        self.user_implement.add_user(new_user)

        return UserResponse(
            success=True,
            user=new_user
        )
   
    def find_user_by_email(self, email: UserEmailRequest) -> UserEmailResponse:
        user = self.user_implement.get_user_by_email(email)
        if not user:
            return UserEmailResponse(
                success=False,
                error_message="User not found."
            )
        return UserEmailResponse(
            success=True,
            email=user.email,
            id=user.id
        )