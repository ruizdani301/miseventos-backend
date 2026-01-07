from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship

from .event_model import Event
from .session_model import Session


class TimeSlot(SQLModel, table=True):
    __tablename__ = "time_slots"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )

    event_id: UUID = Field(
        foreign_key="events.id",
        index=True
    )

    start_time: datetime
    end_time: datetime

    is_assigned: bool = Field(default=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    event: Optional[Event] = Relationship(back_populates="time_slots")

    # Relación 1–1: un slot puede tener solo una sesión
    session: Optional["Session"] = Relationship(back_populates="time_slot")
