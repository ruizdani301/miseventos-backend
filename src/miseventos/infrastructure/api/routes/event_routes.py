from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from miseventos.infrastructure.persistence.postgresql.implement.event_implemet import (
    EventImplement,
)
from miseventos.use_case.event_usecase import EventUseCase
from miseventos.infrastructure.api.controllers.event_controller import (
    add_event_controller,
    find_by_title_controller,
    all_events_controller,
    delete_event_controller,
    update_event_controller,
    get_all_events_controller,
    get_events_slot_controller,
    get_events_not_slot_controller
)
from miseventos.entitis.event import EventEntity
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import (
    EventRequest,EventUpdateRequest
)


def register_eventcase(db: Session = Depends(get_db)):
    repo = EventImplement(db)
    return EventUseCase(repo)


event_router = APIRouter(tags=["Eventos"])


@event_router.post("/event/")
async def register_event(
    body: EventRequest, usecase: EventUseCase = Depends(register_eventcase)
): 
    """Registra un nuevo evento."""
    
    response = add_event_controller(usecase)
    print(response.__dict__)
    
    return await response(body)


@event_router.get("/event/{title}")
async def get_event_by_title(
    title: str, usecase: EventUseCase = Depends(register_eventcase)
):
    """Busca un evento por su título."""
    response = find_by_title_controller(usecase)
    return await response(title)


@event_router.get("/event/")
async def get_all_events(
    page: int = 1, limit: int = 10, usecase: EventUseCase = Depends(register_eventcase)
):
    """Obtiene una lista paginada de todos los eventos."""
    response = all_events_controller(usecase)
    return await response(page, limit)


@event_router.delete("/event/{event_id}")
async def delete_event(
    event_id: UUID, usecase: EventUseCase = Depends(register_eventcase)
):  
    """Elimina un evento por su ID."""
    
    response = delete_event_controller(usecase)
    return await response(event_id)

@event_router.put("/event/")
async def update_event(
    body: EventUpdateRequest, usecase: EventUseCase = Depends(register_eventcase)
): 
    """Actualiza la información de un evento existente."""
    
    response = update_event_controller(usecase)
    
    return await response(body)

@event_router.get("/event/all/")
async def get_all_events_paginated(
    page: int = 1, limit: int = 10, usecase: EventUseCase = Depends(register_eventcase)
):
    """Obtiene eventos con detalles de sesiones y oradores, paginados."""
    response = get_all_events_controller(usecase)
    return await response(page, limit)

@event_router.get("/event/slot/")
async def get_events_slot(
    usecase: EventUseCase = Depends(register_eventcase)
):
    """Obtiene la relación de eventos y sus franjas horarias."""
    response = get_events_slot_controller(usecase)
    return await response()

@event_router.get("/simple/")
async def get_events_without_slot(
    usecase: EventUseCase = Depends(register_eventcase)
):
    """Obtiene eventos que no tienen asignada una franja horaria."""
    response = get_events_not_slot_controller(usecase)
    return await response()