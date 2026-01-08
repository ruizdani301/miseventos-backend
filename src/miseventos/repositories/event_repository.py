from abc import ABC, abstractmethod
from miseventos.entitis.event import EventEntity
from uuid import UUID
from typing import List
from miseventos.infrastructure.persistence.postgresql.schemas.schema import Response


class EventRepository(ABC):
    @abstractmethod
    def add_event(self, event: EventEntity) -> EventEntity:
        pass

    @abstractmethod
    def get_events_paginated(self, page: int, limit: int) -> List[EventEntity] | None:
        pass

    @abstractmethod
    def get_event_by_title(self, event_title: str) -> List[EventEntity] | None:
        pass

    @abstractmethod
    def del_event(self, event_id: UUID) -> Response:
        pass
