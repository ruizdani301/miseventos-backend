from miseventos.use_case.speaker_usecase import SpeakerUseCase
from fastapi import HTTPException
from miseventos.infrastructure.persistence.postgresql.schemas.speaker_schema import (
    SpeakerResponse,
    SpeakerDeleteResponse,
)


def save_speaker_controller(usecase: SpeakerUseCase):
    async def controller(speaker) -> SpeakerResponse:
        response = usecase.add_speaker(speaker)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def get_speakers_by_event_id_controller(usecase: SpeakerUseCase):
    async def controller(event_id) -> SpeakerResponse:
        response = usecase.get_speakers_by_event_id(event_id)
        if not response.success:
            raise HTTPException(status_code=404, detail=response.error_message)
        return response

    return controller


def delete_speaker_controller(usecase: SpeakerUseCase):
    async def controller(speaker_id) -> SpeakerDeleteResponse:
        print("en controller delete speaker")
        print(speaker_id)
        response = usecase.delete_speaker(speaker_id)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def update_speaker_controller(usecase: SpeakerUseCase):
    async def controller(speaker) -> SpeakerResponse:
        response = usecase.update_speaker(speaker)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller
