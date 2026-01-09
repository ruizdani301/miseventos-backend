from miseventos.repositories.event_repository import EventRepository
from miseventos.entitis.event import EventEntity
from sqlalchemy import orm, func
from miseventos.infrastructure.persistence.postgresql.models.event_model import (
    Event as EventModel,
)
from miseventos.infrastructure.persistence.postgresql.models.session_model import Session
from miseventos.infrastructure.persistence.postgresql.models.time_model import TimeSlot
from miseventos.infrastructure.persistence.postgresql.models.speaker_model import Speaker
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName
from miseventos.infrastructure.persistence.postgresql.models.session_speaker_model import SessionSpeaker
from uuid import UUID
from typing import List


class EventImplement(EventRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def add_event(self, event: EventEntity) -> EventEntity:
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
    ):
        try:
        
            offset = (page - 1) * limit

            #event_models = self.session.query(EventModel).offset(offset).limit(limit).all()
            # Calcular offset
        
        
            # Query principal
            query = (
                self.session.query(
                    EventModel,
                    Session,
                    TimeSlot,
                    Speaker
                )
                .select_from(EventModel)
                .outerjoin(Session, EventModel.id == Session.event_id)
                .outerjoin(TimeSlot, Session.time_slot_id == TimeSlot.id)
                .outerjoin(SessionSpeaker, Session.id == SessionSpeaker.session_id)
                .outerjoin(Speaker, SessionSpeaker.speaker_id == Speaker.id)
                .filter(EventModel.status == "PUBLISHED")
                .order_by(
                    EventModel.start_date.desc(),
                    TimeSlot.start_time.asc().nulls_first(),
                    Session.title.asc().nulls_first(),
                    Speaker.full_name.asc().nulls_first()
                )
                .offset(offset)
                .limit(limit)
            )
            
            # Contar total
            total_query = self.session.query(func.count(EventModel.id)).filter(EventModel.status == "PUBLISHED")
            total = total_query.scalar()
            
            # Ejecutar
            results = query.all()

            # Procesar resultados
            events_dict = {}
            for event, session_obj, time_slot, speaker in results:
                event_id = str(event.id)
                
                if event_id not in events_dict:
                    events_dict[event_id] = {
                        "event": event,
                        "sessions": {}
                    }
                
                # Si hay sesión
                if session_obj:
                    session_id = str(session_obj.id)
                    if session_id not in events_dict[event_id]["sessions"]:
                        events_dict[event_id]["sessions"][session_id] = {
                            "session": session_obj,
                            "time_slot": time_slot,
                            "speakers": []
                        }
                    
                    # Si hay speaker, añadirlo a la sesión
                    if speaker:
                        events_dict[event_id]["sessions"][session_id]["speakers"].append(speaker)
            
            # Convertir a lista
            processed_results = []
            for event_data in events_dict.values():
                sessions_list = []
                for session_data in event_data["sessions"].values():
                    sessions_list.append({
                        "session": session_data["session"],
                        "time_slot": session_data["time_slot"],
                        "speakers": session_data["speakers"]
                    })
                
                processed_results.append({
                    "event": event_data["event"],
                    "sessions": sessions_list
                })

            return {
                "data": processed_results,
                "total": total,
                "page": page,
                "page_size": limit,
                "total_pages": (total + limit - 1) // limit
            }
        except:
            self.session.rollback()
            return None

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
                self.session.query(
                    EventModel,
                    Session,
                    TimeSlot,
                    Speaker
                )
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
                    Speaker.full_name.asc().nulls_first()
                )
                
            )
            
            # Contar total
            total_query = self.session.query(func.count(EventModel.id)).filter(EventModel.status == "PUBLISHED")
            total = total_query.scalar()
            
            # Ejecutar
            results = query.all()

            # Procesar resultados
            events_dict = {}
            for event, session_obj, time_slot, speaker in results:
                event_id = str(event.id)
                
                if event_id not in events_dict:
                    events_dict[event_id] = {
                        "event": event,
                        "sessions": {}
                    }
                
                # Si hay sesión
                if session_obj:
                    session_id = str(session_obj.id)
                    if session_id not in events_dict[event_id]["sessions"]:
                        events_dict[event_id]["sessions"][session_id] = {
                            "session": session_obj,
                            "time_slot": time_slot,
                            "speakers": []
                        }
                    
                    if speaker:
                        events_dict[event_id]["sessions"][session_id]["speakers"].append(speaker)
            
            # Convertir a lista
            processed_results = []
            for event_data in events_dict.values():
                sessions_list = []
                for session_data in event_data["sessions"].values():
                    sessions_list.append({
                        "session": session_data["session"],
                        "time_slot": session_data["time_slot"],
                        "speakers": session_data["speakers"]
                    })
                
                processed_results.append({
                    "event": event_data["event"],
                    "sessions": sessions_list
                })
            print("POR TITULO")
            print(processed_results)
            return {
                "data": processed_results,
            }
        except:
            self.session.rollback()
            return None

    def del_event(self, event_id: UUID) -> UUID:
        event_model = self.session.query(EventModel).filter_by(id=event_id).first()
        if event_model:
            self.session.delete(event_model)
            self.session.commit()
            return event_id
        return None
