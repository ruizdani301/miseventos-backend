from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from miseventos.entitis.speaker import SpeakerEntity
from miseventos.infrastructure.persistence.postgresql.schemas.speaker_schema import (
     ResponseSimpleSpeaker,
     SpeakerUpdateRequest)


class SpeakerRepository(ABC):
    @abstractmethod
    def add_speaker(self, speaker: SpeakerEntity) -> ResponseSimpleSpeaker:
        pass

    @abstractmethod
    def get_speaker_by_event_id(self, event_id: UUID) -> List[SpeakerEntity] | None:
        pass

    @abstractmethod
    def delete_speaker(self, speaker_id: UUID) -> UUID:
        pass

    @abstractmethod
    def update_speaker(self, speaker: SpeakerUpdateRequest) -> SpeakerEntity:
        pass

    @abstractmethod
    def get_speaker(self,) -> List[SpeakerEntity] | None:
            pass
