from abc import ABC, abstractmethod
from miseventos.entitis.time_slot import TimeSlotEntity
from uuid import UUID
from typing import List
from miseventos.infrastructure.persistence.postgresql.schemas.schema import Response


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
