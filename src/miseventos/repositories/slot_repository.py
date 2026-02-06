from abc import ABC, abstractmethod
from miseventos.entitis.time_slot import TimeSlotEntity
from uuid import UUID
from typing import List
from miseventos.infrastructure.persistence.postgresql.schemas.schema import Response
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    GetSlotsEventResponse,
    SlotUpdateRequest,
    SlotGroupResponse,
    SlotGroupUpdate,
)


class SlotRepository(ABC):
    @abstractmethod
    def add_slot(self, slot: TimeSlotEntity) -> TimeSlotEntity:
        pass

    @abstractmethod
    def get_slot_by_event_id(self, event_id: UUID) -> List[TimeSlotEntity] | None:
        pass

    @abstractmethod
    def delete_slot(self, event_id: UUID) -> Response:
        pass

    @abstractmethod
    def get_all_slot(self, page: int, limit: int) -> GetSlotsEventResponse:
        pass

    @abstractmethod
    def update_slots_batch(self, slots: SlotUpdateRequest) -> SlotGroupUpdate:
        pass
