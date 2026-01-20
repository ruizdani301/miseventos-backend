from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from miseventos.use_case.session_usecase import SessionUseCase
from miseventos.infrastructure.api.controllers.speaker_controller import (
    save_speaker_controller,
    get_speakers_by_event_id_controller,
    delete_speaker_controller,
    update_speaker_controller,
    get_speakers_controller
)
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import (
    SessionRequest,
)
from miseventos.infrastructure.persistence.postgresql.implement.speaker_implement import (
    SpeakerImplement,
)
from miseventos.use_case.speaker_usecase import SpeakerUseCase
from miseventos.infrastructure.persistence.postgresql.schemas.speaker_schema import (
    SpeakerRequest,
    SpeakerUpdateRequest,
)


def register_speakercase(db: Session = Depends(get_db)):
    repo = SpeakerImplement(db)
    return SpeakerUseCase(repo)


speaker_router = APIRouter()


@speaker_router.post("/speaker/")
async def register_speaker(
    body: SpeakerRequest, usecase: SpeakerUseCase = Depends(register_speakercase)
):
    response = save_speaker_controller(usecase)
    return await response(body)


@speaker_router.get("/speaker/{event_id}")
async def get_speakers_by_event_id(
    event_id: UUID, usecase: SpeakerUseCase = Depends(register_speakercase)
    ):
    """
        Endpoint con logica realizada pendiente de implementación
        :param event_id: ID del evento
        :type event_id: UUID
      
    """
    
    response = get_speakers_by_event_id_controller(usecase)
    return await response(event_id)


@speaker_router.delete("/speaker/{speaker_id}")
async def delete_speaker(
    speaker_id: UUID, usecase: SpeakerUseCase = Depends(register_speakercase)
):
    response = delete_speaker_controller(usecase)
    return await response(speaker_id)


@speaker_router.put("/speaker/")
async def update_speaker(
    body: SpeakerUpdateRequest, usecase: SpeakerUseCase = Depends(register_speakercase)
):
    response = update_speaker_controller(usecase)
    return await response(body)


@speaker_router.get("/speaker/")
async def get_speakers(
    usecase: SpeakerUseCase = Depends(register_speakercase)
):
    
    response = get_speakers_controller(usecase)
    return await response()