from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel

from .session_model import Session
from .speaker_model import Speaker


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
