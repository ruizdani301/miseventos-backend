from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime
from typing import List
from typing import Optional
from datetime import time

class SessionRequest(SQLModel):
    title: str
    description: str
    event_id: UUID
    capacity: int
    time_slot_id: UUID
    speaker_id : str



class ResponseSession(SQLModel):
    id: Optional[str] | UUID
    title: str
    description: str
    created_at: datetime
    event_id: UUID
    capacity: int
    time_slot_id: Optional[UUID]


class SessionResponse(SQLModel):
    success: bool
    error_message: str | None = None
    session: ResponseSession | List[ResponseSession] | None = None


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
    speaker_id : str
   

