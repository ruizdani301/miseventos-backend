from dataclasses import dataclass, field
from datetime import datetime
from ..infrastructure.persistence.postgresql.models.enum import EventStatus
from uuid import UUID
from typing import Optional


@dataclass
class SessionEntity:
    id: Optional[str] = None
    title: str = None
    description: str = None
    created_at: datetime = None
    event_id: Optional[str] = None
    time_slot_id: list[str] = None
    capacity: int = 0
