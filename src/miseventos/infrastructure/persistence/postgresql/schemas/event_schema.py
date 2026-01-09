from miseventos.entitis.event import EventEntity
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field
from miseventos.infrastructure.persistence.postgresql.models.enum import EventStatus
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import ResponseSession
from miseventos.infrastructure.persistence.postgresql.schemas.speaker_schema import ResponseSpeaker
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import SlotResponse
from uuid import UUID
class EventData(SQLModel):
    id: Optional[str] | UUID = None  # UUID como string
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

class SessionNestedResponse(SQLModel):
    session: ResponseSession
    time_slot: SlotResponse
    speakers: List[ResponseSpeaker]

class EventNestedResponse(SQLModel):
    event: EventData
    sessions: List[SessionNestedResponse]

class EventsCompletedResponse(SQLModel):
    success:bool
    error_message: str | None
    total: int | None
    page: int | None
    page_size: int | None
    total_pages: int | None
    events:List[EventNestedResponse] | None
   

