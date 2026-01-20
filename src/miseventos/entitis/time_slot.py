from dataclasses import dataclass
from datetime import datetime, time
from uuid import UUID
from typing import Optional
from uuid import UUID
from fastapi import HTTPException


@dataclass
class TimeSlotEntity:
    id: Optional[str] = None
    event_id: UUID = None
    start_time: time = None
    end_time: time = None
    created_at: datetime = None
    is_assigned: bool = False


    def validate_time_slot(self) -> None:
        if not self.start_time or not self.end_time:
            raise HTTPException(
                status_code=400,
                detail="start_time and end_time are required"
            )

        if self.start_time >= self.end_time:
            raise HTTPException(
                status_code=400,
                detail="start_time must be earlier than end_time"
            )

