from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import orm
from sqlalchemy.orm import joinedload

from miseventos.entitis.sessions import SessionEntity
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session as SessionModel,
)
from miseventos.infrastructure.persistence.postgresql.models.session_speaker_model import (
    SessionSpeaker,
)
from miseventos.infrastructure.persistence.postgresql.models.speaker_model import (
    Speaker,
)
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import (
    ResponseSessionSpeaker,
    SessionRequest,
    SessionUpdateRequest,
)
from miseventos.repositories.session_repository import SessionRepository


class SessionImplement(SessionRepository):
    def __init__(self, session: orm.Session):
        self.session: orm.Session = session

    def add_session(self, body: SessionRequest) -> SessionModel:
        try:
            speaker_id = UUID(body.speaker_id)

            speaker = (
                self.session.query(Speaker).filter(Speaker.id == speaker_id).first()
            )

            if not speaker:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Speaker no encontrado",
                )

            new_session_model = SessionModel(
                title=body.title,
                description=body.description,
                event_id=body.event_id,
                capacity=body.capacity,
                time_slot_id=body.time_slot_id,
            )

            self.session.add(new_session_model)
            self.session.flush()

            new_session_model.session_speakers.append(
                SessionSpeaker(speaker_id=speaker_id)
            )

            self.session.commit()
            self.session.refresh(new_session_model)
            return new_session_model

        except Exception:
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creando la sesión",
            )

    def get_session_by_event_id(self, event_id: UUID) -> List[SessionEntity] | None:
        try:
            session_models = (
                self.session.query(SessionModel)
                .filter(SessionModel.event_id == event_id)
                .all()
            )
            if session_models:
                return [
                    SessionEntity(
                        id=str(session_model.id),
                        title=session_model.title,
                        description=session_model.description,
                        created_at=session_model.created_at,
                        event_id=str(session_model.event_id),
                        capacity=session_model.capacity,
                        time_slot_id=session_model.time_slot_id,
                    )
                    for session_model in session_models
                ]
            return None
        except Exception as e:
            raise e

    def delete_session(self, body_id: UUID) -> UUID:
        try:
            session_model = (
                self.session.query(SessionModel)
                .filter(SessionModel.id == body_id)
                .first()
            )
            if session_model:
                self.session.delete(session_model)
                self.session.commit()
                return body_id
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def update_session(self, body: SessionUpdateRequest) -> SessionModel:

        session_model = (
            self.session.query(SessionModel).filter(SessionModel.id == body.id).first()
        )

        if not session_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Session no encontrada"
            )

        new_speaker_id = UUID(body.speaker_id)

        speaker = (
            self.session.query(Speaker).filter(Speaker.id == new_speaker_id).first()
        )

        if not speaker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Speaker no encontrado"
            )

        session_model.title = body.title
        session_model.description = body.description
        session_model.capacity = body.capacity
        session_model.event_id = body.event_id
        session_model.time_slot_id = body.time_slot_id

        current_speaker_id = (
            session_model.session_speakers[0].speaker_id
            if session_model.session_speakers
            else None
        )
        try:
            if current_speaker_id != new_speaker_id:
                session_model.session_speakers.clear()
                session_model.session_speakers.append(
                    SessionSpeaker(speaker_id=new_speaker_id)
                )

            self.session.commit()
            self.session.refresh(session_model)
            return session_model
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_sessions(self) -> List[ResponseSessionSpeaker] | None:
        try:
            sessions_models = (
                self.session.query(SessionModel)
                .options(joinedload(SessionModel.session_speakers))
                .all()
            )

            if not sessions_models:
                return []

            response_list = []
            for session_model in sessions_models:
                s_id = None
                if session_model.session_speakers:
                    s_id = str(session_model.session_speakers[0].speaker_id)
                else:
                    print("  - AVISO: Esta sesión NO tiene speakers asociados en la tabla intermedia")

                item = ResponseSessionSpeaker(
                    id=str(session_model.id),
                    title=session_model.title,
                    description=session_model.description or "",
                    created_at=session_model.created_at,
                    event_id=session_model.event_id,
                    capacity=session_model.capacity,
                    time_slot_id=session_model.time_slot_id,
                    speaker_id=s_id
                )
                response_list.append(item)
                
            return response_list

        except Exception as e:
            print(f"Error crítico en get_sessions: {e}")
            return None
