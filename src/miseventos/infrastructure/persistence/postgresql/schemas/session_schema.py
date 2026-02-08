from datetime import datetime, time
from typing import List, Optional
from uuid import UUID

from sqlmodel import SQLModel


class SessionRequest(SQLModel):
    title: str
    description: str
    event_id: UUID
    capacity: int
    time_slot_id: UUID
    speaker_id: str


class ResponseSession(SQLModel):
    id: Optional[str] | UUID
    title: str
    description: str
    created_at: datetime
    event_id: UUID
    capacity: int
    time_slot_id: Optional[UUID]

class ResponseSessionSpeaker(SQLModel):
    id: Optional[str] | UUID
    title: str
    description: str
    created_at: datetime
    event_id: UUID
    capacity: int
    speaker_id: str
    time_slot_id: Optional[UUID]


class SessionResponse(SQLModel):
    success: bool
    error_message: str | None = None
    session: ResponseSession | List[ResponseSession] | None = None

class SessionSpeakerResponse(SQLModel):
    success: bool
    error_message: str | None = None
    session: List[ResponseSessionSpeaker] | None = None

class SessionDeleteResponse(SQLModel):
    id: UUID
    success: bool
    error_message: str | None = None


class SessionUpdateRequest(SQLModel):
    id: str
    title: str
    description: str
    event_id: UUID | str
    capacity: int
    time_slot_id: UUID | str
    speaker_id: str
