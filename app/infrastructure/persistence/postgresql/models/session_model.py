from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

from .event_model import Event
from .time_model import TimeSlot
from .session_speaker_model import SessionSpeaker
from .session_registration_model import SessionRegistration


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )

    title: str
    description: Optional[str] = None
    capacity: int

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    event_id: UUID = Field(
        foreign_key="events.id",
        index=True
    )

    time_slot_id: UUID = Field(
        foreign_key="time_slots.id",
        unique=True,
        index=True
    )

    event: Optional[Event] = Relationship(back_populates="sessions")
    time_slot: Optional[TimeSlot] = Relationship(back_populates="session")

    speakers: List["SessionSpeaker"] = Relationship(back_populates="session")
    registrations: List["SessionRegistration"] = Relationship(back_populates="session")
