from datetime import datetime, time, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Time, Column, ForeignKey
from .event_model import Event
from .session_model import Session


class TimeSlot(SQLModel, table=True):
    __tablename__ = "time_slots"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    event_id: UUID = Field(
        sa_column=Column(
            ForeignKey("events.id", ondelete="CASCADE"), index=True
        )
    )

    start_time: time = Field(sa_column=Column(Time))
    end_time: time = Field(sa_column=Column(Time))

    is_assigned: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    event: Optional[Event] = Relationship(back_populates="time_slots")

    # Relación 1–1: un slot puede tener solo una sesión
    session: Optional["Session"] = Relationship(back_populates="time_slot")
