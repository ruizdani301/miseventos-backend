"""User authentication and management use case module.

This module contains the UserUseCase class which handles all business logic
related to user management including registration, authentication, CRUD operations,
and password management.
"""

# Standard library imports
from uuid import UUID

# Local application imports
from miseventos.entitis.user import UserEntity
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import (
    UserImplement,
)
from miseventos.infrastructure.persistence.postgresql.schemas.user_schema import (
    LoginRequest,
    LoginResponse,
    LoginTokenResponse,
    UserEmailRequest,
    UserEmailResponse,
    UserListResponse,
    UserRequest,
    UserResponse,
    UserUpdateRequest,
    UserUpdateResponse,
)
from miseventos.repositories.user_repository import UserRepository
from token_jwt.jwt_handler import create_access_token
from utils.cryp_password import encrypt_password, verify_password


class UserUseCase:
    """Use case class for user authentication and management operations.
    
    This class encapsulates all business logic related to users, including
    registration, authentication, password management, and CRUD operations.
    
    Attributes:
        user_implement: Repository implementation for user data access.
    """

    def __init__(self, user_implement: UserImplement):
        """Initialize the UserUseCase.
        
        Args:
            user_implement: The user repository implementation instance.
        """
        self.user_implement = user_implement

    def save_user(self, request: UserRequest) -> UserResponse:
        """Register a new user in the system.
        
        Validates that no user with the same email exists, validates password
        format, encrypts the password, and persists the user to the database.
        
        Args:
            request: User registration request containing email, password, and role.
        
        Returns:
            UserResponse object with success status and either the created user ID
            or an error message.
        """
        existing_user = self.user_implement.get_user_by_email(request.email)
        if existing_user:
            return UserResponse(
                success=False, error_message="User with this email already exists."
            )
        new_user = UserEntity(
            email=request.email,
            password=request.password,
            role=request.role or "assistant",
        )

        if not new_user.valid_password():
            return UserResponse(
                id=new_user.id, success=False, error_message="Invalid password format."
            )
        new_user.password = encrypt_password(new_user.password)

        response = self.user_implement.add_user(new_user)
        if not response:
            return UserResponse(success=False, error_message="User not found.", id=None)
        return UserResponse(success=True, error_message=None, id=response.id)

    def find_all_users(self) -> UserListResponse:
        """Retrieve all users from the system.
        
        Returns:
            UserListResponse containing list of all users or error message if
            no users found.
        """
        response = self.user_implement.get_users()
        if not response:
            return UserListResponse(
                success=False, error_message="User not found.", users=None
            )
        return UserListResponse(success=True, error_message=None, users=response)

    def update_user(self, request: UserUpdateRequest) -> UserUpdateResponse:
        """Update an existing user's information.
        
        Handles password updates intelligently:
        - If password unchanged, keeps existing encrypted password
        - If password matches existing (already encrypted), keeps it
        - If new password provided, encrypts it before saving
        
        Args:
            request: User update request containing user ID and updated fields.
        
        Returns:
            UserUpdateResponse with success status and updated user or error message.
        """
        existing_user = self.user_implement.get_user_by_id(request.id)
        if not existing_user:
            return UserUpdateResponse(success=False, error_message="User not found.")

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
            role=request.role,
        )
        response = self.user_implement.update_user(new_user)
        if not response:
            return UserUpdateResponse(
                success=False, error_message="User not found.", user=None
            )

        return UserUpdateResponse(success=True, error_message=None, user=response)

    def find_user_by_email(self, email: UserEmailRequest) -> UserEmailResponse:
        """Search for a user by email address.
        
        Args:
            email: Email request object containing the email to search for.
        
        Returns:
            UserEmailResponse with user email and ID or error message if not found.
        """
        user = self.user_implement.get_user_by_email(email.email)
        if not user:
            return UserEmailResponse(success=False, error_message="User not found.")
        return UserEmailResponse(success=True, email=user.email, id=user.id)

    def delete_user(self, id: UUID) -> UserResponse:
        """Delete a user by ID.
        
        Args:
            id: UUID of the user to delete.
        
        Returns:
            UserResponse with success status and deleted user ID or error message.
        """
        response = self.user_implement.delete_user(id)
        if not response:
            return UserResponse(success=False, error_message="User not found.", id=None)
        return UserResponse(success=True, error_message=None, id=response.id)

    def login(self, request: LoginRequest) -> LoginTokenResponse:
        """Authenticate a user and generate JWT access token.
        
        Validates user credentials and generates a JWT token containing user
        information (email, user_id, role) for subsequent authenticated requests.
        
        Args:
            request: Login request containing email and password.
        
        Returns:
            LoginTokenResponse with success status, user information, and JWT
            access token or error message if authentication fails.
        """
        user = self.user_implement.get_user_by_email(request.email)
        if not user:
            return LoginTokenResponse(success=False, error_message="User not found.")

        if not verify_password(request.password, user.password):
            return LoginTokenResponse(success=False, error_message="Invalid password.")

        access_token = create_access_token(
            data={"email": user.email, "user_id": str(user.id), "role": user.role}
        )

        return LoginTokenResponse(
            success=True,
            error_message=None,
            user_id=user.id,
            email=user.email,
            role=user.role,
            access_token=access_token,
        )
