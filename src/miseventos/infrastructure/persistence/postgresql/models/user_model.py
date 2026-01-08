from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from .enum import RoleName


if TYPE_CHECKING:

    from .event_registration_model import EventRegistration
    from .session_registration_model import SessionRegistration


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    __module__ = "miseventos.infrastructure.persistence.postgresql.models.user_model"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    email: str = Field(index=True, unique=True, nullable=False)

    password_hash: str
    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    role: str = Field(default=RoleName.ASSISTANT.value, nullable=False)

    event_registrations: List["EventRegistration"] = Relationship(back_populates="user")

    session_registration: List["SessionRegistration"] = Relationship(
        back_populates="user"
    )
