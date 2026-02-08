from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from miseventos.infrastructure.persistence.postgresql.models.speaker_model import (
        Speaker,
    )

    from .event_model import Event
    from .session_registration_model import SessionRegistration
    from .session_speaker_model import SessionSpeaker
    from .time_model import TimeSlot


class Session(SQLModel, table=True):
    __tablename__ = "sessions"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    title: str
    description: Optional[str] = None
    capacity: int

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    event_id: UUID = Field(
        sa_column=Column(ForeignKey("events.id", ondelete="CASCADE"), index=True)
    )

    time_slot_id: UUID = Field(
        sa_column=Column(
            ForeignKey("time_slots.id", ondelete="CASCADE"), unique=True, index=True
        )
    )

    event: Optional["Event"] = Relationship(back_populates="session")
    time_slot: Optional["TimeSlot"] = Relationship(back_populates="session")

    session_speakers: List["SessionSpeaker"] = Relationship(
        back_populates="session",
        sa_relationship_kwargs={"cascade": "all, delete", "passive_deletes": True},
    )
    registrations: List["SessionRegistration"] = Relationship(
        back_populates="session",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "passive_deletes": True,
        },
    )
