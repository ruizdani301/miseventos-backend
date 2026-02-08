from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from miseventos.entitis.event import EventEntity
from miseventos.infrastructure.api.controllers.event_controller import (
    add_event_controller,
    all_events_controller,
    delete_event_controller,
    find_by_title_controller,
    get_all_events_controller,
    get_events_not_slot_controller,
    get_events_slot_controller,
    update_event_controller,
)
from miseventos.infrastructure.persistence.postgresql.implement.event_implemet import (
    EventImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import (
    EventRequest,
    EventUpdateRequest,
)
from miseventos.use_case.event_usecase import EventUseCase
from token_jwt.jwt_handler import get_current_user


def register_eventcase(db: Session = Depends(get_db)):
    repo = EventImplement(db)
    return EventUseCase(repo)


event_router = APIRouter(tags=["Eventos"])


@event_router.post("/event/")
async def register_event(
    body: EventRequest, usecase: EventUseCase = Depends(register_eventcase)
):
    

    response = add_event_controller(usecase)

    return await response(body)


# @event_router.get("/event/{title}")
# async def get_event_by_title(
#     title: str, usecase: EventUseCase = Depends(register_eventcase)
# ):
#     """Busca un evento por su título."""
#     response = find_by_title_controller(usecase)
#     return await response(title)


@event_router.get("/event/")
async def get_all_events(
    page: int = 1,
    limit: int = 10,
    title: str = None,
    usecase: EventUseCase = Depends(register_eventcase),
    current_user: dict = Depends(get_current_user),
):
    """
    Gets a paginated list of all events

    
    **args:**
    **Returns:**
    ```json
    {
    {
        "success": true,
        "error_message": null,
        "total": 1,
        "page": 1,
        "page_size": 10,
        "total_pages": 1,
        "events": [
            {
            "event": {
                "id": "04d7a0c0-c8ce-4d0e-b8f1-0c7d8bd28952",
                "title": "LA TECNOLOGIA COMO AMIGA DEL HOMBRE",
                "description": "Conversatorio sobre herraminetas q optimicen la vida",
                "start_date": "2026-02-10T08:20:00",
                "end_date": "2026-02-10T12:20:00",
                "capacity": 100,
                "status": "published",
                "created_at": "2026-02-07T23:17:38.091001",
                "registrations_count": 1
            },
            "sessions": [
                {
                "session": {
                    "id": "6188cd6e-7f44-445f-901b-211a524a785d",
                    "title": "como pasar de ser un cantante a un ingeniero",
                    "description": "Es la grandiosa oportunidad de conocer como billy jean dejo ala chica embarazada",
                    "created_at": "2026-02-07T23:47:08.346879",
                    "event_id": "04d7a0c0-c8ce-4d0e-b8f1-0c7d8bd28952",
                    "capacity": 25,
                    "time_slot_id": "4b3ab660-3d9a-4bb1-90dd-d202a80d7a73",
                    "registrations_count": 0,
                    "user_registration_id": null
                },
                "time_slot": {
                    "id": "4b3ab660-3d9a-4bb1-90dd-d202a80d7a73",
                    "start_time": "09:00:00",
                    "end_time": "10:00:00",
                    "event_id": "04d7a0c0-c8ce-4d0e-b8f1-0c7d8bd28952",
                    "is_assigned": true,
                    "created_at": "2026-02-07T23:44:59.904299"
                },
                "speakers": [
                    {
                    "id": "0a6c9e99-6587-4fd3-9c0f-1d93836228c2",
                    "full_name": "ING MAIKOL JAKSON",
                    "email": "maikol@gamil.com",
                    "bio": "Despues de su triunfo por los grandes escenarios se volvio ingeniero",
                    "created_at": "2026-02-07T23:46:02.839166"
                    }
                ]
                }
            ]
            }
        ]
        }
    }

    """
    user_id = UUID(current_user.get("user_id"))
    response = all_events_controller(usecase)
    return await response(page, limit, user_id, title)


@event_router.delete("/event/{event_id}")
async def delete_event(
    event_id: UUID, usecase: EventUseCase = Depends(register_eventcase)
):
    """
    Delete event by id
    **Return**
    ```json
    {
    success: bool,
    error_message: Optional[str] = None,
    id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    }
    """


    response = delete_event_controller(usecase)
    return await response(event_id)


@event_router.put("/event/")
async def update_event(
    body: EventUpdateRequest, usecase: EventUseCase = Depends(register_eventcase)
):
    """
    Update event by id
    - **Return**
    ```json
    {
    success: bool,
    error_message: Optional[str] = None,
    events:{
        id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        title: titulo actual,
        description: description actual,
        start_date: 16:00:00,
        end_date: 17:00:00,
        capacity= 45,
        status: activo,
        created_at: 2026-02-07T23:17:,
        }
    }
    """

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
async def get_events_slot(usecase: EventUseCase = Depends(register_eventcase)):
    """
    Obtains the list of events and their time slots.
    **Return      
    ```json
    success: True,
    error_message: None,
    events:{
        id: "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        title: "titulo del evento",
        time_slot: [
                {
                    "start_time": "16.00.00",
                    "end_time": "17:00:00"
                    }
                ]
        }
        '''
    """
    response = get_events_slot_controller(usecase)
    return await response()


@event_router.get("/simple/")
async def get_events_without_slot(usecase: EventUseCase = Depends(register_eventcase)):
    """Obtiene eventos que no tienen asignada una franja horaria."""
    response = get_events_not_slot_controller(usecase)
    return await response()
