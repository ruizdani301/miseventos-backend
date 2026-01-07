from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship

from .session_model import Session
from .speaker_model import Speaker


class SessionSpeaker(SQLModel, table=True):
    __tablename__ = "session_speakers"

    session_id: UUID = Field(
        foreign_key="sessions.id",
        primary_key=True
    )

    speaker_id: UUID = Field(
        foreign_key="speakers.id",
        primary_key=True
    )

    session: Optional[Session] = Relationship(back_populates="speakers")
    speaker: Optional[Speaker] = Relationship(back_populates="sessions")
