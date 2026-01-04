from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Enum

from .status_model import EventStatus
from .user_model import User
from .session_model import Session
from .time_model import TimeSlot
from .event_registration_model import EventRegistration


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )

    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int

    status: EventStatus = Field(
        sa_column=Enum(EventStatus),
        default=EventStatus.draft
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    created_by: Optional[UUID] = Field(
        default=None,
        foreign_key="users.id"
    )
    creator: Optional[User] = Relationship(back_populates="created_events")

    sessions: List["Session"] = Relationship(back_populates="event")
    time_slots: List["TimeSlot"] = Relationship(back_populates="event")
    registrations: List["EventRegistration"] = Relationship(back_populates="event")
