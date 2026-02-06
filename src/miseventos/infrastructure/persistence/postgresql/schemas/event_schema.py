from miseventos.entitis.event import EventEntity
from typing import Optional, List
from datetime import datetime, time
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
    registrations_count: int | None = None


class ResponseNestedSession(SQLModel):
    id: Optional[str] | UUID
    title: str
    description: Optional[str] = None
    created_at: datetime
    event_id: UUID
    capacity: int
    time_slot_id: Optional[UUID]
    registrations_count: int | None = None
    user_registration_id: Optional[str] | UUID = None

class SessionNestedResponse(SQLModel):
    session: ResponseNestedSession
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

class EventNestedCompletedResponse(SQLModel):
    success:bool
    error_message: str | None
    events:EventsCompletedResponse | None

class EventRequest(SQLModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int = Field(..., gt=0)
    status: EventStatus = EventStatus.PUBLISHED

class EventUpdateRequest(SQLModel):
    id: Optional[str] | UUID = None
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    capacity: int = Field(..., gt=0)
    status: EventStatus = EventStatus.PUBLISHED

class EventSessionResponse(SQLModel):
    id: str
    title : str

class NewTimeRange(SQLModel):
    id:UUID
    start_time: time
    end_time: time

class EventSlotResponse(SQLModel):
    id: UUID
    title : str
    time_slot : List[NewTimeRange]

class EventRespose(SQLModel):
    success: bool
    error_message: str | None
    events: list[EventData] | EventData | None = None

class EventSlotRelationResponse(SQLModel):
    success: bool
    error_message: str | None
    events :  List[EventSlotResponse]

class EventWithOutResponse(SQLModel):
    event_id: UUID
    title : str

class EventNotSlotsResponse(SQLModel):
    success: bool
    error_message: str | None
    events :  List[EventWithOutResponse]