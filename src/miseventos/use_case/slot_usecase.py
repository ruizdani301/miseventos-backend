from miseventos.infrastructure.persistence.postgresql.implement.slot_implement import SlotImplement
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import EventRequest
from miseventos.entitis.time_slot import TimeSlotEntity as SlotEntity
from uuid import UUID
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import SlotRequest
from miseventos.infrastructure.persistence.postgresql.schemas.schema import Response
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import SlotSaveResponse, SlotDeleteResponse
class SlotUseCase:
    def __init__(self, slot_implement: SlotImplement):
        self.slot_implement = slot_implement

    def save_slot(self, request: SlotRequest)->SlotSaveResponse:
        new_slot = SlotEntity(
            start_time=request.start_time,
            end_time=request.end_time,
            event_id=request.event_id,
            is_assigned=request.is_assigned,
            
        )
        slot_saved = self.slot_implement.add_slot(new_slot)
        if not slot_saved:
            return SlotSaveResponse(
                success=False,
                error_message="Error saving slot."
            )

        return SlotSaveResponse(
            success=True,
            error_message=None,
            slot=slot_saved
        )

    def get_slot_by_event_id(self, event_id:UUID) -> SlotSaveResponse:
        slots_list = self.slot_implement.get_slot_by_event_id(event_id=event_id)
        print("UseCase Slots List:", slots_list)
        if not slots_list:
            return SlotSaveResponse(
                success=False,
                error_message="No slots found for the given event ID."
            )
        return SlotSaveResponse(
            success=True,
            error_message=None,
            slot=slots_list
        )
    def delete_slot(self, event_id: UUID)->SlotDeleteResponse:
        response = self.slot_implement.delete_slot(event_id)
        if not response.success:
            return SlotDeleteResponse(
                success=False,
                error_message=response.error_message
            )
        return SlotDeleteResponse(
            id=response.id,
            success=True,
            error_message=None
        )
    