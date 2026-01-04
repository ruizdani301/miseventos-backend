from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

from .roles_model import Role
from .event_model import Event
from .event_registration_model import EventRegistration
from .session_registration_model import SessionRegistration


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )

    email: str = Field(
        index=True,
        unique=True,
        nullable=False
    )

    password_hash: str
    is_active: bool = Field(default=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    role_id: Optional[UUID] = Field(
        default=None,
        foreign_key="roles.id",
        index=True
    )

    role: Optional[Role] = Relationship(back_populates="users")

    created_events: List["Event"] = Relationship(back_populates="creator")

    event_registrations: List["EventRegistration"] = Relationship(
        back_populates="user"
    )

    session_registrations: List["SessionRegistration"] = Relationship(
        back_populates="user"
    )
