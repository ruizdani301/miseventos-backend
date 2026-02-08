from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from miseventos.infrastructure.api.controllers.slot_controller import (
    add_slot_controller,
    all_slots_controller,
    delete_slot_controller,
    find_slot_by_event_id_controller,
    update_slots_batch_controller,
)
from miseventos.infrastructure.persistence.postgresql.implement.slot_implement import (
    SlotImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    SlotRequest,
    SlotUpdateRequest,
)
from miseventos.use_case.event_usecase import EventUseCase
from miseventos.use_case.slot_usecase import SlotUseCase
from token_jwt.jwt_handler import get_current_user


def register_slotcase(db: Session = Depends(get_db)):
    repo = SlotImplement(
        db
    )  
    return SlotUseCase(repo)  


slot_router = APIRouter(tags=["Intervalos de tiempo"])


@slot_router.post("/slot/")
async def register_slot(
    body: SlotRequest,
    usecase: SlotUseCase = Depends(register_slotcase),
    current_user: dict = Depends(get_current_user),
):
    """Crea uno o varios intervalos de tiempo asociados a un evento."""
    response = add_slot_controller(usecase)
    return await response(body)


@slot_router.delete("/slot/{slot_id}")
async def delete_slot(
    slot_id: UUID,
    usecase: SlotUseCase = Depends(register_slotcase),
    current_user: dict = Depends(get_current_user),
):
    """Elimina un intervalo de tiempo por su ID."""
    response = delete_slot_controller(usecase)
    return await response(slot_id)


@slot_router.get("/slot/{event_id}")
async def get_slot_by_event_id(
    event_id: UUID, usecase: SlotUseCase = Depends(register_slotcase)
):
    """
    Get all the slot time from each session by even_id.
    **Returns**
    ```json
    {
    "success": True,
    "error_message": None,
    "events":[
    {
                    "id":"jkhdfauisasd7fndfob",
                    "start_time": "2022-01-01T00:00:00",
                    "end_time": "2022-01-01T00:00:00",
                    "event_id":"jkhdfauisasd7fndfob",
                    "capacity":100,
                    "is_assigned":True,
                    "created_at":"2022-01-01T00:00:00",
                }
            ]
    }
    """
    response = find_slot_by_event_id_controller(usecase)
    return await response(event_id)


@slot_router.get("/slot/")
async def get_all_slots(
    page: int = 1,
    limit: int = 10,
    usecase: SlotUseCase = Depends(register_slotcase),
    current_user: dict = Depends(get_current_user),
):
    """
    Get all the slot time from each session by even_id.
    **Returns**
    ```json
    {
    "success": True,
    "error_message": None,
    "events":[
                    "id":"jkhdfauisasd7fndfob",
                    "title":"el titulo del evento",
                    "description":"la descripcion del evento",
                    "start_date":"2022-01-01T00:00:00",
                    "capacity":100,
                    "time_slots":[
                        {
                            "start_time": "2022-01-01T00:00:00",
                            "end_time": "2022-01-01T00:00:00",
                        }
                        ]
    }
    """
    response = all_slots_controller(usecase)
    return await response(page, limit)


@slot_router.put("/slot/")
async def update_slots_batch(
    body: SlotUpdateRequest,
    usecase: SlotUseCase = Depends(register_slotcase),
    current_user: dict = Depends(get_current_user),
):
    """Actualiza un intervalo de tiempo por su ID."""
    response = update_slots_batch_controller(usecase)
    return await response(body)
