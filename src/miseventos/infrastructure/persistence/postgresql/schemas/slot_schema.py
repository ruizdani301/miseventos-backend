from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime, time
from typing import List, Optional


class SlotRequest(SQLModel):
    start_time: time
    end_time: time
    event_id: UUID
    is_assigned: bool = False


class SlotResponse(SQLModel):
    id: UUID
    start_time: time
    end_time: time
    event_id: UUID
    is_assigned: bool
    created_at: datetime


class SlotSaveResponse(SQLModel):
    success: bool
    error_message: str | None = None
    slot: SlotResponse | List[SlotResponse] | None = None


class SlotDeleteResponse(SQLModel):
    id: UUID
    success: bool
    error_message: str | None = None
