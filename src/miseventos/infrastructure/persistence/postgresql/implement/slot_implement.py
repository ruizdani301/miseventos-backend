from miseventos.entitis.time_slot import TimeSlotEntity
from miseventos.repositories.slot_repository import SlotRepository
from sqlalchemy import orm
from miseventos.infrastructure.persistence.postgresql.models.time_model import (
    TimeSlot as TimeSlotModel,
)
from miseventos.infrastructure.persistence.postgresql.schemas.schema import Response
from uuid import UUID
from typing import List
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    SlotDeleteResponse,
)
from sqlalchemy import and_


class SlotImplement(SlotRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def add_slot(self, slot: TimeSlotEntity) -> TimeSlotEntity | None:
        """
        Agrega un nuevo slot si no hay solapamiento con slots existentes.
        Retorna None si hay conflicto.
        """

        # 2. Buscar slots existentes que se solapen
        existing_slots = (
            self.session.query(TimeSlotModel)
            .filter(
                and_(
                    TimeSlotModel.event_id == slot.event_id,
                    TimeSlotModel.start_time < slot.end_time,
                    TimeSlotModel.end_time > slot.start_time,
                )
            )
            .first()
        )

        if existing_slots:
            # Ya existe un slot que se solapa
            return None

        # 3. Crear y guardar el nuevo slot
        new_slot_model = TimeSlotModel(
            start_time=slot.start_time,
            end_time=slot.end_time,
            event_id=slot.event_id,
            is_assigned=slot.is_assigned or False,
        )

        self.session.add(new_slot_model)
        self.session.commit()
        self.session.refresh(new_slot_model)

        return TimeSlotEntity(
            id=str(new_slot_model.id),
            start_time=new_slot_model.start_time,
            end_time=new_slot_model.end_time,
            event_id=new_slot_model.event_id,
            is_assigned=new_slot_model.is_assigned,
            created_at=new_slot_model.created_at,
        )

    def get_slot_by_event_id(self, event_id: UUID) -> List[TimeSlotEntity] | None:

        slot_models = (
            self.session.query(TimeSlotModel)
            .filter(TimeSlotModel.event_id == event_id)
            .all()
        )

        if slot_models:
            return [
                TimeSlotEntity(
                    id=str(slot_model.id),
                    start_time=slot_model.start_time,
                    end_time=slot_model.end_time,
                    event_id=slot_model.event_id,
                    is_assigned=slot_model.is_assigned,
                    created_at=slot_model.created_at,
                )
                for slot_model in slot_models
            ]
        return None

    def delete_slot(self, slot_id: UUID) -> Response:
        slot_models = self.session.query(TimeSlotModel).filter(
            TimeSlotModel.id == slot_id
        )
        if slot_models.first() is None:
            return SlotDeleteResponse(
                success=False, error_message="No slots found for the given event ID."
            )
        slot_models.delete()
        self.session.commit()
        return SlotDeleteResponse(id=slot_id, success=True, error_message=None)
