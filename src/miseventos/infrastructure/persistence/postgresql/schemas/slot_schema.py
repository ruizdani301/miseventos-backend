from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime, time
from typing import List, Optional

class TimeRange(SQLModel):
    start_time: time
    end_time: time

class SlotRequest(SQLModel):
    event_id: UUID
    time_slots:List[TimeRange]
    is_assigned: bool = False


class SlotResponse(SQLModel):
    id: UUID
    start_time: time
    end_time: time
    event_id: UUID
    is_assigned: bool
    created_at: datetime


class SlotDeleteResponse(SQLModel):
    id: UUID
    success: bool
    error_message: str | None = None

class SlotRangeResponse(SQLModel):
    start_time: str
    end_time: str

class SlotGroupResponse(SQLModel):
    id: str
    event_id: UUID | str
    is_assigned: bool
    slots: List[SlotRangeResponse]
    created_at: datetime

class SlotGroupSaveResponse(SQLModel):
    success: bool
    error_message: str | None = None
    slot: SlotGroupResponse | List[SlotGroupResponse] | None = None


class GetSlotsEventResponse(SQLModel):
    id: UUID | str
    title: str
    description: Optional[str]
    start_date: datetime
    capacity: int
    time_slots: List[SlotRangeResponse]


class SlotSaveResponse(SQLModel):
    success: bool
    error_message: str | None = None
    slot: SlotResponse | List[SlotResponse] | List[GetSlotsEventResponse] | None = None

class SlotEventsResponse(SQLModel):
    success: bool
    error_message: str | None = None
    events:  List[GetSlotsEventResponse] | None = None
