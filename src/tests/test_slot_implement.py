from datetime import datetime
from uuid import uuid4

import pytest

from miseventos.infrastructure.persistence.postgresql.implement.slot_implement import (
    SlotImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.event_model import (
    Event as EventModel,
)
from miseventos.infrastructure.persistence.postgresql.models.time_model import (
    TimeSlot as TimeSlotModel,
)
from miseventos.infrastructure.persistence.postgresql.schemas.slot_schema import (
    SlotGroupUpdate,
    SlotUpdateRequest,
)


def test_add_slot(db_session):
    # Arrange
    repository = SlotImplement(db_session)
    event = EventModel(title="Event", description="Desc", status="PUBLISHED")
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    slot_data = TimeSlotModel(
        event_id=event.id,
        start_time=datetime(2023, 10, 1, 10, 0),
        end_time=datetime(2023, 10, 1, 11, 0),
        is_assigned=False
    )

    # Act
    result = repository.add_slot([slot_data])

    # Assert
    assert result.event_id == event.id
    assert len(result.slots) == 1
    assert db_session.query(TimeSlotModel).count() == 1

def test_get_slot_by_event_id(db_session):
    # Arrange
    repository = SlotImplement(db_session)
    event_id = uuid4()
    slot = TimeSlotModel(
        event_id=event_id,
        start_time=datetime.now(),
        end_time=datetime.now(),
        is_assigned=False
    )
    db_session.add(slot)
    db_session.commit()

    # Act
    result = repository.get_slot_by_event_id(event_id)

    # Assert
    assert len(result) == 1
    assert result[0].event_id == event_id

def test_delete_slot(db_session):
    # Arrange
    repository = SlotImplement(db_session)
    slot = TimeSlotModel(
        event_id=uuid4(),
        start_time=datetime.now(),
        end_time=datetime.now(),
        is_assigned=False
    )
    db_session.add(slot)
    db_session.commit()
    db_session.refresh(slot)

    # Act
    result = repository.delete_slot(slot.id)

    # Assert
    assert result.success is True
    assert db_session.query(TimeSlotModel).filter_by(id=slot.id).first() is None

def test_get_all_slot_pagination(db_session):
    # Arrange
    repository = SlotImplement(db_session)
    event = EventModel(title="E1", description="D", status="PUBLISHED")
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    
    slot = TimeSlotModel(event_id=event.id, start_time=datetime.now(), end_time=datetime.now())
    db_session.add(slot)
    db_session.commit()

    # Act
    result = repository.get_all_slot(page=1, limit=10)

    # Assert
    assert len(result) == 1
    assert result[0].title == "E1"
    assert len(result[0].time_slots) == 1
