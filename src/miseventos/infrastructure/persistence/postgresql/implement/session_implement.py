from miseventos.entitis.sessions import SessionEntity
from uuid import UUID
from typing import List
from sqlalchemy import orm
from miseventos.repositories.session_repository import SessionRepository
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session as SessionModel,
)


class SessionImplement(SessionRepository):
    def __init__(self, session: orm.Session):
        self.session: orm.Session = session

    def add_session(self, body: SessionEntity) -> SessionEntity:

        new_session_model = SessionModel(
            title=body.title,
            description=body.description,
            event_id=body.event_id,
            capacity=body.capacity,
            time_slot_id=body.time_slot_id,
        )
        self.session.add(new_session_model)
        self.session.commit()
        self.session.refresh(new_session_model)
        return SessionEntity(
            id=str(new_session_model.id),
            title=new_session_model.title,
            description=new_session_model.description,
            created_at=new_session_model.created_at,
            event_id=str(new_session_model.event_id),
            capacity=new_session_model.capacity,
            time_slot_id=new_session_model.time_slot_id,
        )

    def get_session_by_event_id(self, event_id: UUID) -> List[SessionEntity] | None:

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

    def delete_session(self, body_id: UUID) -> UUID:
        session_model = (
            self.session.query(SessionModel).filter(SessionModel.id == body_id).first()
        )
        if session_model:
            self.session.delete(session_model)
            self.session.commit()
            return body_id
        return None

    def update_session(self, body: SessionEntity) -> SessionEntity:
        session_model = (
            self.session.query(SessionModel).filter(SessionModel.id == body.id).first()
        )
        if session_model:
            session_model.title = body.title
            session_model.description = body.description
            session_model.capacity = body.capacity
            session_model.time_slot_id = body.time_slot_id
            session_model.event_id = body.event_id
            self.session.commit()
            self.session.refresh(session_model)
        return SessionEntity(
            id=str(session_model.id),
            title=session_model.title,
            description=session_model.description,
            created_at=session_model.created_at,
            event_id=str(session_model.event_id),
            capacity=session_model.capacity,
            time_slot_id=session_model.time_slot_id,
        )
