from fastapi import HTTPException
from miseventos.use_case.slot_usecase import SlotUseCase
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.schema import Response
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    SlotResponse,SlotEventsResponse
)
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    SlotRequest,
)
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    SlotSaveResponse,
)


def add_slot_controller(usecase: SlotUseCase):
    async def controller(body: SlotRequest) -> SlotResponse:
        response = usecase.save_slot(body)

        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)

        return response

    return controller


def find_slot_by_event_id_controller(usecase: SlotUseCase):
    async def controller(event_id: UUID) -> SlotSaveResponse:
        response = usecase.get_slot_by_event_id(event_id)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        print("Controller Response:", response)
        return response

    return controller


def delete_slot_controller(usecase: SlotUseCase):
    async def controller(slot_id: UUID) -> Response:
        response = usecase.delete_slot(slot_id)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller


def all_slots_controller(usecase: SlotUseCase):
    async def controller(page: int, limit: int)-> SlotEventsResponse :
        response = usecase.get_slot_all(page=page, limit=limit)
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error_message)
        return response

    return controller
