from typing import Optional, List
from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName


class UserRequest(SQLModel):
    email: str
    password: str
    role: Optional[str] = RoleName.ASSISTANT.value

class UserUpdateRequest(SQLModel):
    id: UUID
    email: str
    password: str
    role: Optional[str] = RoleName.ASSISTANT.value

class UserUpdateRequest(SQLModel):
    id: UUID | None = None
    email: str
    password: str
    role: Optional[str] = RoleName.ASSISTANT.value

class UserResponse(SQLModel):
    id: UUID | None = None
    success: bool
    error_message: Optional[str] = None

class updateResponse(SQLModel):
    id: UUID | None = None
    email: str | None = None
    role: str | None = None

class UserUpdateResponse(SQLModel):
    success: bool
    error_message: Optional[str] = None
    user: updateResponse | None = None


class UserEmailRequest(SQLModel):
    email: str


class UserEmailResponse(SQLModel):
    id: UUID
    email: str
    success: bool
    error_message: Optional[str] = None


class LoginRequest(SQLModel):
    email: str
    password: str


class LoginTokenResponse(SQLModel):
    success: bool
    error_message: Optional[str] = None
    user_id: UUID | None = None
    email: str | None = None
    role: str | None = None
    access_token: str | None = None

class LoginResponse(SQLModel):
    success: bool
    error_message: Optional[str] = None
    user_id: UUID
    email: str
    role: str

class UserAllResponse(SQLModel):
    id: UUID
    email: str
    password: str
    role: str
    

class UserListResponse(SQLModel):
    success: bool
    error_message: Optional[str] = None
    users: List[UserAllResponse] | None = None


