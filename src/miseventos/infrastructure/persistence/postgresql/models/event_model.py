from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from .enum import EventStatus

if TYPE_CHECKING:
    from .event_registration_model import EventRegistration
    from .session_model import Session
    from .time_model import TimeSlot


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int

    status: EventStatus = Field(default=EventStatus.PUBLISHED)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    session: List["Session"] = Relationship(
        back_populates="event",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
    time_slots: List["TimeSlot"] = Relationship(
        back_populates="event",
        sa_relationship_kwargs={
            "cascade": "delete, delete-orphan",
            "passive_deletes": True,
        },
    )
    registrations: List["EventRegistration"] = Relationship(
        back_populates="event",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
