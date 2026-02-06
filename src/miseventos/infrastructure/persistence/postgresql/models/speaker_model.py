from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:

    from .session_speaker_model import SessionSpeaker


class Speaker(SQLModel, table=True):
    __tablename__ = "speakers"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    full_name: str
    email: Optional[str] = Field(default=None, index=True)
    bio: Optional[str] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    speaker_sessions: List["SessionSpeaker"] = Relationship(
        back_populates="speaker",
        sa_relationship_kwargs={"cascade": "all, delete", "passive_deletes": True},
    )
