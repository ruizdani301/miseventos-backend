from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel
from miseventos.entitis.event import EventEntity


class Response(SQLModel):
    id: Optional[UUID] = None
    success: bool
    error_message: Optional[str] = None
    event: Optional[EventEntity] = None
