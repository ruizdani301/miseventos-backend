from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column, ForeignKey

from .user_model import User
from .session_model import Session


class SessionRegistration(SQLModel, table=True):
    __tablename__ = "session_registrations"
    __table_args__ = (
        UniqueConstraint("user_id", "session_id", name="uq_user_session"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    user_id: UUID = Field(foreign_key="users.id", index=True)

    session_id: UUID = Field(
        sa_column=Column(ForeignKey("sessions.id", ondelete="CASCADE"), index=True)
    )

    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional[User] = Relationship(back_populates="session_registration")
    session: Optional[Session] = Relationship(back_populates="registrations")
