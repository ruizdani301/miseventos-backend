from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, ForeignKey
from .session_model import Session
from .speaker_model import Speaker
from uuid import uuid4
from uuid import UUID


class SessionSpeaker(SQLModel, table=True):
    __tablename__ = "session_speakers"

    session_id: UUID = Field(
        sa_column=Column(
            ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True
        )
    )

    speaker_id: UUID = Field(
        sa_column=Column(
            ForeignKey("speakers.id", ondelete="CASCADE"), primary_key=True
        )
    )

    session: Optional["Session"] = Relationship(back_populates="session_speakers")
    speaker: Optional["Speaker"] = Relationship(back_populates="speaker_sessions")
