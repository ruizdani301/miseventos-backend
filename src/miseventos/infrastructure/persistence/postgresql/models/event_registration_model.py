from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint, Column, ForeignKey
from .event_model import Event

if TYPE_CHECKING:
    from .user_model import User


class EventRegistration(SQLModel, table=True):
    __tablename__ = "event_registrations"
    __table_args__ = (UniqueConstraint("user_id", "event_id", name="uq_user_event"),)

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    user_id: UUID = Field(foreign_key="users.id", index=True)
    event_id: UUID = Field(
        sa_column=Column(
            ForeignKey("events.id", ondelete="CASCADE"), index=True
        )
    )

    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="event_registrations")
    event: Optional[Event] = Relationship(back_populates="registrations")
