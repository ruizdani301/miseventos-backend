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
    SlotDeleteResponse, SlotGroupResponse, SlotRangeResponse, GetSlotsEventResponse,SlotUpdateRequest, SlotGroupUpdateResponse, SlotGroupUpdate, SlotRangeIdResponse
)
from miseventos.infrastructure.persistence.postgresql.models.time_model import TimeSlot
from miseventos.infrastructure.persistence.postgresql.models.event_model import Event
#from sqlmodel import select
from sqlalchemy import select
from sqlalchemy.orm import selectinload



class SlotImplement(SlotRepository):
    def __init__(self, session: orm.Session):
        self.session = session

    def add_slot(self, slots: List[TimeSlot]) -> SlotGroupResponse | None:
        try:
            list_slots: List[TimeSlot] = []
            for slot in slots:
                new_slot = TimeSlot(
                    event_id=slot.event_id,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    is_assigned=slot.is_assigned,
                )
                list_slots.append(new_slot)

            self.session.add_all(list_slots)
            self.session.commit()

            for each_slot in list_slots:
                self.session.refresh(each_slot)


            return SlotGroupResponse(
                id=str(list_slots[0].id),
                event_id=list_slots[0].event_id,
                is_assigned=list_slots[0].is_assigned,
                created_at=list_slots[0].created_at,
                slots=[
                    SlotRangeResponse(
                        start_time=slot.start_time.isoformat(),
                        end_time=slot.end_time.isoformat(),
                    )
                    for slot in list_slots
                ],
            )
        except Exception as e:
            self.session.rollback()
            raise e

    def get_slot_by_event_id(self, event_id: UUID) -> List[TimeSlotEntity] | None:
        try:
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
        except Exception as e:
            raise e

    def delete_slot(self, slot_id: UUID) -> Response:
        try:
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
        except Exception as e:
            self.session.rollback()
            raise e


    def get_all_slot(self, page: int, limit: int) -> List[GetSlotsEventResponse]:
        offset = (page - 1) * limit

        try:
            statement = (
            select(Event)
            .options(selectinload(Event.time_slot))
            .order_by(Event.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
            events = self.session.execute(statement).scalars().all()
            return [
                GetSlotsEventResponse(
                    id=event.id,
                    title=event.title,
                    description=event.description,
                    start_date=event.start_date,
                    capacity=event.capacity,
                    time_slots=[
                        SlotRangeResponse(
                            start_time=slot.start_time.isoformat(),
                            end_time=slot.end_time.isoformat(),
                        )
                        for slot in event.time_slot
                    ]
                )
                for event in events
            ]
        except Exception as e:
            raise e

    def update_slots_batch(self, slots_data: SlotUpdateRequest) -> SlotGroupUpdate | None:
        try:
            exists = self.session.query(TimeSlotModel).filter(
                TimeSlotModel.event_id == slots_data.event_id
            ).first()

            if not exists:
                return None

            updated_slots = []
            for slot_item in slots_data.time_slots:
                db_slot = self.session.query(TimeSlotModel).filter(
                    TimeSlotModel.id == slot_item.id,
                    TimeSlotModel.event_id == slots_data.event_id 
                ).first()

                if db_slot:
                    db_slot.start_time = slot_item.start_time
                    db_slot.end_time = slot_item.end_time
                    db_slot.is_assigned = slots_data.is_assigned
                    updated_slots.append(db_slot)

            self.session.commit()

            if not updated_slots:
                return None

            return SlotGroupUpdate(
                event_id=slots_data.event_id,
                is_assigned=slots_data.is_assigned,
                created_at=updated_slots[0].created_at,
                slots=[
                    SlotRangeIdResponse(
                        id=slot.id,
                        start_time=slot.start_time.isoformat(),
                        end_time=slot.end_time.isoformat(),
                    )
                    for slot in updated_slots
                ],
            )
        except Exception as e:
            self.session.rollback()
            raise e
