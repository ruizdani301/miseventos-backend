from sqlalchemy import orm
from miseventos.repositories.speaker_repository import SpeakerRepository
from miseventos.infrastructure.persistence.postgresql.models.speaker_model import (
    Speaker as SpeakerModel,
)
from miseventos.entitis.speaker import SpeakerEntity
from uuid import UUID
from typing import List
from miseventos.infrastructure.persistence.postgresql.models.session_speaker_model import (
    SessionSpeaker,
)
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session,
)
from miseventos.infrastructure.persistence.postgresql.schemas.speaker_schema import (
    ResponseSimpleSpeaker,
    SpeakerUpdateRequest
)


class SpeakerImplement(SpeakerRepository):
    def __init__(self, session: orm.Session):
        self._session = session

    def add_speaker(self, speaker: SpeakerEntity) -> ResponseSimpleSpeaker:
        try:
            new_speaker_model = SpeakerModel(
                full_name=speaker.full_name, email=speaker.email, bio=speaker.bio
            )
            self._session.add(new_speaker_model)
            self._session.commit()
            self._session.refresh(new_speaker_model)
            return ResponseSimpleSpeaker(
                id=str(new_speaker_model.id),
                #full_name=new_speaker_model.full_name,
                #bio=new_speaker_model.bio,
                #email=new_speaker_model.email,
                created_at=new_speaker_model.created_at,
            )
        except Exception as e:
            self._session.rollback()
            raise e

    def get_speaker_by_event_id(self, event_id: UUID) -> List[SpeakerEntity] | None:
        try:
            speaker_models = (
                self._session.query(SpeakerModel)
                .join(
                    SessionSpeaker, SpeakerModel.id == SessionSpeaker.speaker_id
                )  # Join con tabla intermedia
                .join(
                    Session, SessionSpeaker.session_id == Session.id
                )  # Join con Session
                .filter(Session.event_id == event_id)  # Ahora sí podemos filtrar
                .distinct()
                .all()
            )

            if not speaker_models:
                return None

            return [
                SpeakerEntity(
                    id=str(speaker_model.id),
                    full_name=speaker_model.full_name,
                    bio=speaker_model.bio,
                    email=speaker_model.email,
                    created_at=speaker_model.created_at,
                )
                for speaker_model in speaker_models
            ]

        except Exception as e:
            self._session.rollback()
            raise e

    def delete_speaker(self, speaker_id: UUID) -> UUID:
        try:
            speaker_model = (
                self._session.query(SpeakerModel)
                .filter(SpeakerModel.id == speaker_id)
                .first()
            )
            if speaker_model:
                self._session.delete(speaker_model)
                self._session.commit()
                return speaker_id
            return None
        except Exception as e:
            self._session.rollback()
            raise e

    def update_speaker(self, speaker: SpeakerUpdateRequest) -> SpeakerEntity:
        try:
            speaker_model = (
                self._session.query(SpeakerModel)
                .filter(SpeakerModel.id == speaker.id)
                .first()
            )
            if speaker_model:

                speaker_model.email = speaker.email
                speaker_model.full_name = speaker.full_name
                speaker_model.bio = speaker.bio
                self._session.commit()
                self._session.refresh(speaker_model)
                return SpeakerEntity(
                    id=str(speaker_model.id),
                    full_name=speaker_model.full_name,
                    bio=speaker_model.bio,
                    email=speaker_model.email,
                    created_at=speaker_model.created_at,
                )
        except Exception as e:
            self._session.rollback()
            raise e
    

    def get_speaker(self,) -> List[SpeakerEntity] | None:
        try: 
            speaker_model = (
                self._session.query(SpeakerModel)
                .order_by(SpeakerModel.full_name.desc())
                .all()
            )
            return [SpeakerEntity(
                id=speaker.id,
                email=speaker.email,
                full_name = speaker.full_name,
                bio=speaker.bio,
                created_at=speaker.created_at
            )
                for speaker in speaker_model ]
        
        except Exception as e:
            raise e

