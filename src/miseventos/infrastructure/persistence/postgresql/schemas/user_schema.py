from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName


class UserRequest(SQLModel):
    email: str
    password: str
    role: Optional[str] = RoleName.ASSISTANT.value


class UserResponse(SQLModel):
    id: UUID | None = None
    success: bool
    error_message: Optional[str] = None


class UserEmailRequest(SQLModel):
    email: str


class UserEmailResponse(SQLModel):
    id: UUID
    email: str
    success: bool
    error_message: Optional[str] = None
