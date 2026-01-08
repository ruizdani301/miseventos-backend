from miseventos.entitis.event import EventEntity
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from miseventos.infrastructure.persistence.postgresql.models.enum import EventStatus


class EventData(SQLModel):
    id: Optional[str] = None  # UUID como string
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int
    status: EventStatus
    created_at: Optional[datetime] = None


class EventRespose(SQLModel):
    success: bool
    error_message: str | None
    events: list[EventData] | None


class EventRequest(SQLModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int = Field(..., gt=0)
    status: EventStatus = EventStatus.PUBLISHED
