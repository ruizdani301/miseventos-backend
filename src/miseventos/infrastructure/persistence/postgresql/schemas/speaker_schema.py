from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime
from typing import List
from typing import Optional


class SpeakerRequest(SQLModel):
    full_name: str
    email: str
    bio: str


class ResponseSpeaker(SQLModel):
    id: UUID
    full_name: str
    email: str
    bio: str
    created_at: datetime

class ResponseSimpleSpeaker(SQLModel):
     id: UUID
     created_at: datetime


class SpeakerResponse(SQLModel):
    success: bool
    error_message: str | None = None
    speaker: ResponseSimpleSpeaker | List[ResponseSimpleSpeaker] | ResponseSpeaker | List[ResponseSpeaker] | None = None


class SpeakerDeleteResponse(SQLModel):
    id: UUID
    success: bool
    error_message: str | None = None


class SpeakerUpdateRequest(SQLModel):
    id: UUID
    full_name: str
    email: str
    bio: str


class SpeakerEventResponse(SQLModel):
    success: bool
    error_message: str | None = None
    event_id: str | None = None
    speaker: ResponseSpeaker | List[ResponseSpeaker] | None = None

