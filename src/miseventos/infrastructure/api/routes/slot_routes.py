from miseventos.infrastructure.persistence.postgresql.models.database import get_db
from sqlmodel import Session
from fastapi import APIRouter, Depends
from miseventos.infrastructure.persistence.postgresql.implement.slot_implement import (
    SlotImplement,
)
from miseventos.use_case.event_usecase import EventUseCase
from miseventos.use_case.slot_usecase import SlotUseCase
from uuid import UUID
from miseventos.infrastructure.api.controllers.slot_controller import (
    add_slot_controller,
    find_slot_by_event_id_controller,
    delete_slot_controller,
    all_slots_controller,
    update_slots_batch_controller
)
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    SlotRequest, SlotUpdateRequest
)


def register_slotcase(db: Session = Depends(get_db)):
    repo = SlotImplement(
        db
    )  # instancia de UserImplement con la sesión de la base de datos
    return SlotUseCase(repo)  # instancia de UserUseCase con el con user implement


slot_router = APIRouter(tags=["Intervalos de tiempo"])


@slot_router.post("/slot/")
async def register_slot(
    body: SlotRequest, usecase: SlotUseCase = Depends(register_slotcase)
):  
    """Crea uno o varios intervalos de tiempo asociados a un evento."""
    response = add_slot_controller(usecase)
    return await response(body)


@slot_router.delete("/slot/{slot_id}")
async def delete_slot(slot_id: UUID, usecase: SlotUseCase = Depends(register_slotcase)):
    """Elimina un intervalo de tiempo por su ID."""
    response = delete_slot_controller(usecase)
    return await response(slot_id)


@slot_router.get("/slot/{event_id}")
async def get_slot_by_event_id(
    event_id: UUID, usecase: SlotUseCase = Depends(register_slotcase)
):
    """Obtiene todos los intervalos de tiempo asociados a un ID de evento."""
    response = find_slot_by_event_id_controller(usecase)
    return await response(event_id)

@slot_router.get("/slot/")
async def get_all_slots(
    page: int = 1, limit: int = 10, usecase: SlotUseCase = Depends(register_slotcase)
):  
    """Obtiene una lista paginada de eventos con sus intervalos de tiempo."""
    response = all_slots_controller(usecase)
    return await response(page, limit)

@slot_router.put("/slot/")
async def update_slots_batch(
    body: SlotUpdateRequest, usecase: SlotUseCase = Depends(register_slotcase)
):
    """Actualiza un intervalo de tiempo por su ID."""
    response = update_slots_batch_controller(usecase)
    return await response(body)