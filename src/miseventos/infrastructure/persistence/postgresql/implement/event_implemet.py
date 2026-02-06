from miseventos.repositories.event_repository import EventRepository
from miseventos.entitis.event import EventEntity
from sqlalchemy import orm, func
from miseventos.infrastructure.persistence.postgresql.models.event_model import (
    Event as EventModel,
)
from miseventos.infrastructure.persistence.postgresql.models.event_registration_model import (
    EventRegistration,
)
from miseventos.infrastructure.persistence.postgresql.models.session_registration_model import (
    SessionRegistration,
)
from sqlalchemy.orm import load_only
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import (
    EventSlotResponse,
    NewTimeRange,
    EventWithOutResponse,
    EventsCompletedResponse,
)
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session,
)
from miseventos.infrastructure.persistence.postgresql.models.time_model import TimeSlot
from miseventos.infrastructure.persistence.postgresql.models.speaker_model import (
    Speaker,
)
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName
from miseventos.infrastructure.persistence.postgresql.models.session_speaker_model import (
    SessionSpeaker,
)
from uuid import UUID
from typing import List


class EventImplement(EventRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def add_event(self, event: EventEntity) -> EventEntity:
        try:
            new_event_model = EventModel(
                title=event.title,
                description=event.description,
                start_date=event.start_date,
                end_date=event.end_date,
                capacity=event.capacity,
                status=(
                    event.status.value
                    if hasattr(event.status, "value")
                    else event.status
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
        except Exception as e:
            self.session.rollback()
            raise e

    def get_events(self, page: int = 1, limit: int = 10) -> List[EventEntity]:
        offset = (page - 1) * limit

        try:
            query = (
                self.session.query(EventModel)
                .order_by(EventModel.start_date.desc())
                .offset(offset)
                .limit(limit)
            ).all()

            return [
                EventEntity(
                    id=str(event.id),
                    title=event.title,
                    description=event.description,
                    start_date=event.start_date,
                    end_date=event.end_date,
                    capacity=event.capacity,
                    status=event.status,
                    created_at=event.created_at,
                )
                for event in query
            ]

        except Exception as e:
            self.session.rollback()
            raise e

    def get_events_paginated(
        self, page: int = 1, limit: int = 10, user_id: UUID = None, title: str = None
    ) -> EventsCompletedResponse:
        try:
            offset = (page - 1) * limit

            # 1. Subconsultas para los contadores (Correlated Subqueries)
            event_count_sub = (
                self.session.query(func.count(EventRegistration.id))
                .filter(EventRegistration.event_id == EventModel.id)
                .correlate(EventModel)
                .as_scalar()
                .label("event_reg_count")
            )

            session_count_sub = (
                self.session.query(func.count(SessionRegistration.id))
                .filter(SessionRegistration.session_id == Session.id)
                .correlate(Session)
                .as_scalar()
                .label("session_reg_count")
            )

            # 2. Query Principal con Joins estrictos (Inner Joins)
            # Esto filtra automáticamente eventos sin sesiones y sesiones sin speakers
            query = (
                self.session.query(
                    EventModel,
                    Session,
                    TimeSlot,
                    Speaker,
                    event_count_sub,
                    session_count_sub,
                    SessionRegistration.id,
                )
                .join(Session, EventModel.id == Session.event_id)
                .join(TimeSlot, Session.time_slot_id == TimeSlot.id)
                .join(SessionSpeaker, Session.id == SessionSpeaker.session_id)
                .join(Speaker, SessionSpeaker.speaker_id == Speaker.id)
                .outerjoin(
                    SessionRegistration,
                    (
                        (SessionRegistration.session_id == Session.id)
                        & (SessionRegistration.user_id == user_id)
                        if user_id
                        else SessionRegistration.session_id == Session.id
                    ),
                )
                .filter(EventModel.status == "PUBLISHED")
            )

            # Contar total de eventos únicos (siguiendo la misma lógica de joins)
            total_query = (
                self.session.query(func.count(func.distinct(EventModel.id)))
                .join(Session, EventModel.id == Session.event_id)
                .join(SessionSpeaker, Session.id == SessionSpeaker.session_id)
                .filter(EventModel.status == "PUBLISHED")
            )

            # Apply dynamic title filter if provided
            if title:
                query = query.filter(EventModel.title.ilike(f"%{title}%"))
                total_query = total_query.filter(EventModel.title.ilike(f"%{title}%"))

            # Order and Pagination
            query = (
                query.order_by(
                    EventModel.start_date.desc(),
                    TimeSlot.start_time.asc().nulls_first(),
                    Session.title.asc(),
                    Speaker.full_name.asc(),
                )
                .offset(offset)
                .limit(limit)
            )

            total = total_query.scalar() or 0

            results = query.all()

            # 4. Procesamiento de Resultados
            events_dict = {}
            for (
                event,
                session_obj,
                time_slot,
                speaker,
                ev_count,
                sess_count,
                user_reg_id,
            ) in results:
                event_id = str(event.id)

                if event_id not in events_dict:
                    # Creamos el diccionario del evento inyectando el contador
                    event_info = (
                        event.model_dump()
                        if hasattr(event, "model_dump")
                        else event.__dict__.copy()
                    )
                    event_info["registrations_count"] = ev_count or 0

                    events_dict[event_id] = {"event": event_info, "sessions": {}}

                session_id = str(session_obj.id)
                if session_id not in events_dict[event_id]["sessions"]:
                    # Creamos el diccionario de la sesión inyectando el contador
                    session_info = (
                        session_obj.model_dump()
                        if hasattr(session_obj, "model_dump")
                        else session_obj.__dict__.copy()
                    )
                    session_info["registrations_count"] = sess_count or 0
                    session_info["user_registration_id"] = (
                        str(user_reg_id) if user_reg_id else None
                    )

                    events_dict[event_id]["sessions"][session_id] = {
                        "session": session_info,
                        "time_slot": time_slot,
                        "speakers": [],
                    }

                # Añadir speaker (ya garantizado por el join)
                events_dict[event_id]["sessions"][session_id]["speakers"].append(
                    speaker
                )

            # 5. Formatear a lista para el JSON final
            processed_events = []
            for e_data in events_dict.values():
                sessions_list = []
                for s_data in e_data["sessions"].values():
                    sessions_list.append(s_data)

                processed_events.append(
                    {"event": e_data["event"], "sessions": sessions_list}
                )

            return {
                "success": True,
                "error_message": None,
                "total": total,
                "page": page,
                "page_size": limit,
                "total_pages": (total + limit - 1) // limit if total > 0 else 0,
                "data": processed_events,
            }

        except Exception as e:
            self.session.rollback()
            return {"success": False, "error_message": str(e), "total": 0, "data": []}

    # pendiente de revision, se hizo un cambio en get_events_paginated por lo tanto esta ya no sea necesaria
    def get_event_by_title(self, event_title: str) -> List[EventEntity]:
        """
        Para get_event_by_title

        :param self: Descripción
        :param event_title: Descripción
        :type event_title: str
        :return: Descripción
        :rtype: List[EventEntity]
        """
        try:
            query = (
                self.session.query(EventModel, Session, TimeSlot, Speaker)
                .select_from(EventModel)
                .outerjoin(Session, EventModel.id == Session.event_id)
                .outerjoin(TimeSlot, Session.time_slot_id == TimeSlot.id)
                .outerjoin(SessionSpeaker, Session.id == SessionSpeaker.session_id)
                .outerjoin(Speaker, SessionSpeaker.speaker_id == Speaker.id)
                .filter(EventModel.status == "PUBLISHED")
                .filter(EventModel.title.ilike(f"%{event_title}%"))
                .order_by(
                    EventModel.start_date.desc(),
                    TimeSlot.start_time.asc().nulls_first(),
                    Session.title.asc().nulls_first(),
                    Speaker.full_name.asc().nulls_first(),
                )
            )

            # Contar total
            total_query = self.session.query(func.count(EventModel.id)).filter(
                EventModel.status == "PUBLISHED"
            )
            total = total_query.scalar()

            # Ejecutar
            results = query.all()

            # Procesar resultados
            events_dict = {}
            for event, session_obj, time_slot, speaker in results:
                event_id = str(event.id)

                if event_id not in events_dict:
                    events_dict[event_id] = {"event": event, "sessions": {}}

                # Si hay sesión
                if session_obj:
                    session_id = str(session_obj.id)
                    if session_id not in events_dict[event_id]["sessions"]:
                        events_dict[event_id]["sessions"][session_id] = {
                            "session": session_obj,
                            "time_slot": time_slot,
                            "speakers": [],
                        }

                    if speaker:
                        events_dict[event_id]["sessions"][session_id][
                            "speakers"
                        ].append(speaker)

            # Convertir a lista
            processed_results = []
            for event_data in events_dict.values():
                sessions_list = []
                for session_data in event_data["sessions"].values():
                    sessions_list.append(
                        {
                            "session": session_data["session"],
                            "time_slot": session_data["time_slot"],
                            "speakers": session_data["speakers"],
                        }
                    )

                processed_results.append(
                    {"event": event_data["event"], "sessions": sessions_list}
                )

            return {
                "data": processed_results,
            }
        except:
            self.session.rollback()
            return None

    def del_event(self, event_id: UUID) -> UUID:
        try:
            event_model = self.session.query(EventModel).filter_by(id=event_id).first()
            if event_model:
                self.session.delete(event_model)
                self.session.commit()
                return event_id
            return None
        except Exception as e:
            self.session.rollback()
            raise e

    def event_by_simple_title(self, s_title: str) -> EventEntity:
        try:
            event = self.session.query(EventModel).filter_by(title=s_title).first()
            return event
        except Exception as e:
            raise e

    def update_event(self, request: EventEntity) -> EventEntity:
        try:
            event_model = (
                self.session.query(EventModel)
                .filter(EventModel.id == request.id)
                .first()
            )

            if event_model:
                event_model.title = request.title
                event_model.description = request.description
                event_model.start_date = request.start_date
                event_model.end_date = request.end_date
                event_model.capacity = request.capacity
                event_model.status = request.status

                self.session.commit()
                self.session.refresh(event_model)
                return EventEntity(
                    id=str(event_model.id),
                    title=event_model.title,
                    description=event_model.description,
                    start_date=event_model.start_date,
                    end_date=event_model.end_date,
                    capacity=event_model.capacity,
                    status=event_model.status,
                    created_at=event_model.created_at,
                )
        except Exception as e:
            return e

    def get_event_slot_relation(
        self,
    ) -> List[EventSlotResponse]:

        try:
            data = (
                self.session.query(EventModel)
                .outerjoin(TimeSlot)
                .options(
                    load_only(EventModel.id, EventModel.title),
                    orm.selectinload(EventModel.time_slots).load_only(
                        TimeSlot.id, TimeSlot.start_time, TimeSlot.end_time
                    ),
                )
                .distinct()
            )

            return [
                EventSlotResponse(
                    id=event.id,
                    title=event.title,
                    time_slot=[
                        NewTimeRange(
                            id=slot.id,
                            start_time=slot.start_time,
                            end_time=slot.end_time,
                        )
                        for slot in event.time_slots
                    ],
                )
                for event in data
            ]
        except Exception as e:
            return e

    def get_event_not_in_timeslot(
        self,
    ) -> List[EventWithOutResponse]:

        try:
            data = (
                self.session.query(EventModel)
                .outerjoin(TimeSlot, TimeSlot.event_id == EventModel.id)
                .filter(TimeSlot.id == None)
                .options(load_only(EventModel.id, EventModel.title))
                .all()
            )

            return [
                EventWithOutResponse(
                    event_id=event.id,
                    title=event.title,
                )
                for event in data
            ]
        except Exception as e:
            return e
