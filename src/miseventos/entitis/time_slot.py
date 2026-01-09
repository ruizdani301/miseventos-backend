from dataclasses import dataclass
from datetime import datetime, time
from uuid import UUID
from typing import Optional
from uuid import UUID


@dataclass
class TimeSlotEntity:
    id: Optional[str] = None
    event_id: UUID = None
    start_time: time = None
    end_time: time = None
    created_at: datetime = None
    is_assigned: bool = False

    def validate_time_slot(self) -> bool:
        if self.start_time and self.end_time:
            return self.start_time < self.end_time
        return False
