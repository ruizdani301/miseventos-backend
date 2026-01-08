from dataclasses import dataclass, field
from datetime import datetime
from ..infrastructure.persistence.postgresql.models.enum import EventStatus
from uuid import UUID
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class EventEntity:
    id: Optional[str] = None
    title: str = None
    description: str = None
    start_date: datetime = None
    end_date: datetime = None
    capacity: int = 0
    status: EventStatus = EventStatus.PUBLISHED
    created_at: datetime = None

    def validate_dates(self) -> bool:
        if self.start_date and self.end_date:
            return self.start_date < self.end_date
        return False  # O lanza una excepción

    def is_capacity_valid(self) -> bool:
        return self.capacity > 0 and self.capacity <= 1000
