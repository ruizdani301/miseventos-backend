
from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from miseventos.infrastructure.persistence.postgresql.implement.event_implemet import EventImplement
from miseventos.use_case.event_usecase import EventUseCase
from miseventos.infrastructure.api.controllers.event_controller import add_event_controller, find_by_title_controller, all_events_controller, delete_event_controller
from miseventos.entitis.event import EventEntity
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import EventRequest

def register_eventcase(db:Session=Depends(get_db)):
    repo = EventImplement(db) 
    return EventUseCase(repo)
event_router = APIRouter()


@event_router.post("/event/")
async def register_event(body: EventRequest, usecase: EventUseCase = Depends(register_eventcase)):
    response =  add_event_controller(usecase)
    print("en controller event")
    print(response.__dict__)
    return await response(body)

@event_router.get("/event/{title}")
async def get_event_by_title(title: str, usecase: EventUseCase = Depends(register_eventcase)):
    response = find_by_title_controller(usecase)
    return await response(title)

@event_router.get("/events/")
async def get_all_events(page: int = 1, limit: int = 10, usecase: EventUseCase = Depends(register_eventcase)):
    response = all_events_controller(usecase)
    return await response(page, limit)

@event_router.delete("/event/{event_id}")
async def delete_event(event_id: UUID, usecase: EventUseCase = Depends(register_eventcase)):
    response = delete_event_controller(usecase)
    return await response(event_id)

