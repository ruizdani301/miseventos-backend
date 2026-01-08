from abc import ABC, abstractmethod
from miseventos.entitis.sessions import SessionEntity
from uuid import UUID
from typing import List


class SessionRepository(ABC):
    @abstractmethod
    def add_session(self, session: SessionEntity) -> SessionEntity:
        pass

    @abstractmethod
    def get_session_by_event_id(self, event_id: UUID) -> List[SessionEntity] | None:
        pass

    @abstractmethod
    def delete_session(self, session_id: UUID) -> UUID:
        pass

    @abstractmethod
    def update_session(self, session: SessionEntity) -> SessionEntity:
        pass
