from miseventos.repositories.event_repository import EventRepository
from miseventos.entitis.event import EventEntity
from sqlalchemy import orm
from miseventos.infrastructure.persistence.postgresql.models.event_model import (
    Event as EventModel,
)
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName
from uuid import UUID
from typing import List


class EventImplement(EventRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def add_event(self, event: EventEntity) -> EventEntity:
        print("GUARADR IMPLEMENTACION")
        print(event)
        new_event_model = EventModel(
            title=event.title,
            description=event.description,
            start_date=event.start_date,
            end_date=event.end_date,
            capacity=event.capacity,
            status=(
                event.status.value if hasattr(event.status, "value") else event.status
            ),
        )
        self.session.add(new_event_model)
        self.session.commit()
        self.session.refresh(new_event_model)
        return EventEntity(
            id=str(new_event_model.id),
            title=new_event_model.title,
            description=new_event_model.description,
            start_date=new_event_model.start_date,
            end_date=new_event_model.end_date,
            capacity=new_event_model.capacity,
            status=new_event_model.status,
            created_at=new_event_model.created_at,
        )

    def get_events_paginated(
        self, page: int = 1, limit: int = 10
    ) -> List[EventEntity] | None:

        offset = (page - 1) * limit

        event_models = self.session.query(EventModel).offset(offset).limit(limit).all()

        if event_models:
            return [
                EventEntity(
                    id=str(event_model.id),
                    title=event_model.title,
                    description=event_model.description,
                    start_date=event_model.start_date,
                    end_date=event_model.end_date,
                    capacity=event_model.capacity,
                    status=event_model.status,
                    created_at=event_model.created_at,
                )
                for event_model in event_models
            ]
        return None

    def get_event_by_title(self, event_title: str) -> List[EventEntity]:
        event_models = (
            self.session.query(EventModel)
            .filter(EventModel.title.ilike(f"{event_title}%"))
            .all()
        )

        return [
            EventEntity(
                id=str(event_model.id),
                title=event_model.title,
                description=event_model.description,
                start_date=event_model.start_date,
                end_date=event_model.end_date,
                capacity=event_model.capacity,
                status=event_model.status,
                created_at=event_model.created_at,
            )
            for event_model in event_models
        ]

    def del_event(self, event_id: UUID) -> UUID:
        event_model = self.session.query(EventModel).filter_by(id=event_id).first()
        if event_model:
            self.session.delete(event_model)
            self.session.commit()
            return event_id
        return None
