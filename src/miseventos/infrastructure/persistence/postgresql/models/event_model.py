from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Enum

from .enum import EventStatus

# from .session_model import Session
# from .time_model import TimeSlot
# from .event_registration_model import EventRegistration

if TYPE_CHECKING:
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

    status: EventStatus = Field(default=EventStatus.PUBLISHED)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    sessions: List["Session"] = Relationship(back_populates="event")
    time_slots: List["TimeSlot"] = Relationship(back_populates="event")
    registrations: List["EventRegistration"] = Relationship(back_populates="event")
