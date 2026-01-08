from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.implement.speaker_implement import (
    SpeakerImplement,
)
from miseventos.infrastructure.persistence.postgresql.schemas.speaker_schema import (
    SpeakerResponse,
    SpeakerDeleteResponse,
    SpeakerEventResponse,
)
from miseventos.entitis.speaker import SpeakerEntity


class SpeakerUseCase:
    def __init__(self, speaker_implement: SpeakerImplement):
        self.speaker_implement = speaker_implement

    def get_speakers_by_event_id(self, event_id) -> SpeakerEventResponse | None:
        data_speaker = self.speaker_implement.get_speaker_by_event_id(event_id)
        if not data_speaker:
            return SpeakerEventResponse(
                success=False, error_message="No speakers found for the given event ID."
            )
        return SpeakerEventResponse(
            event_id=str(event_id),
            success=True,
            error_message=None,
            speaker=data_speaker,
        )

    def add_speaker(self, speaker: SpeakerEntity) -> SpeakerResponse:
        new_speaker = self.speaker_implement.add_speaker(speaker)
        if not new_speaker:
            return SpeakerResponse(success=False, error_message="Error saving speaker.")
        return SpeakerResponse(success=True, error_message=None, speaker=new_speaker)

    def delete_speaker(self, speaker_id: UUID) -> SpeakerDeleteResponse:
        deleted_id = self.speaker_implement.delete_speaker(speaker_id)
        if not deleted_id:
            return SpeakerDeleteResponse(
                success=False, error_message="Error deleting speaker."
            )
        return SpeakerDeleteResponse(id=deleted_id, success=True, error_message=None)

    def update_speaker(self, speaker: SpeakerEntity) -> SpeakerResponse:
        updated_speaker = self.speaker_implement.update_speaker(speaker)
        if not updated_speaker:
            return SpeakerResponse(
                success=False, error_message="Error updating speaker."
            )
        return SpeakerResponse(
            success=True, error_message=None, speaker=updated_speaker
        )
