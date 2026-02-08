from datetime import datetime
from uuid import uuid4

import pytest

from miseventos.entitis.event import EventEntity
from miseventos.infrastructure.persistence.postgresql.implement.event_implemet import (
    EventImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.event_model import (
    Event as EventModel,
)
from miseventos.infrastructure.persistence.postgresql.models.time_model import (
    TimeSlot as TimeSlotModel,
)
from miseventos.infrastructure.persistence.postgresql.schemas.event_schema import (
    EventUpdateRequest,
)


def test_add_event(db_session):
    # Arrange
    repository = EventImplement(db_session)
    event_entity = EventEntity(
        title="Event 1",
        description="Desc",
        start_date=datetime(2023, 10, 1, 10, 0),
        end_date=datetime(2023, 10, 1, 12, 0),
        capacity=100,
        status="PUBLISHED"
    )

    # Act
    result = repository.add_event(event_entity)

    # Assert
    assert result is not None
    assert db_session.query(EventModel).filter_by(title="Event 1").first() is not None

def test_get_events_paginated_with_title_filter(db_session):
    # Arrange
    repository = EventImplement(db_session)
    e1 = EventModel(title="Searchable Event", description="D", status="PUBLISHED", 
                    start_date=datetime.now(), end_date=datetime.now(), capacity=10)
    e2 = EventModel(title="Other Event", description="D", status="PUBLISHED", 
                    start_date=datetime.now(), end_date=datetime.now(), capacity=10)
    db_session.add_all([e1, e2])
    db_session.commit()

    # Act - Search for "Searchable"
    result = repository.get_events_paginated(page=1, limit=10, title="Searchable")

    # Assert
    assert result["total"] == 1
    assert result["data"][0]["title"] == "Searchable Event"

def test_get_event_by_title(db_session):
    # Arrange
    repository = EventImplement(db_session)
    e1 = EventModel(title="Exact Title", description="D", status="PUBLISHED", 
                    start_date=datetime.now(), end_date=datetime.now(), capacity=10)
    db_session.add(e1)
    db_session.commit()

    # Act
    result = repository.get_event_by_title("Exact Title")

    # Assert
    assert result is not None
    assert result["data"][0]["title"] == "Exact Title"

def test_delete_event(db_session):
    # Arrange
    repository = EventImplement(db_session)
    e1 = EventModel(title="Delete Me", description="D", status="PUBLISHED", 
                    start_date=datetime.now(), end_date=datetime.now(), capacity=10)
    db_session.add(e1)
    db_session.commit()
    db_session.refresh(e1)

    # Act
    result = repository.del_event(e1.id)

    # Assert
    assert result == str(e1.id)
    assert db_session.query(EventModel).filter_by(id=e1.id).first() is None

def test_get_event_not_in_timeslot(db_session):
    # Arrange
    repository = EventImplement(db_session)
    e_no_slot = EventModel(title="No Slot", description="D", status="PUBLISHED", 
                          start_date=datetime.now(), end_date=datetime.now(), capacity=10)
    e_with_slot = EventModel(title="With Slot", description="D", status="PUBLISHED", 
                            start_date=datetime.now(), end_date=datetime.now(), capacity=10)
    db_session.add_all([e_no_slot, e_with_slot])
    db_session.commit()
    db_session.refresh(e_no_slot)
    db_session.refresh(e_with_slot)

    slot = TimeSlotModel(event_id=e_with_slot.id, start_time=datetime.now(), end_time=datetime.now())
    db_session.add(slot)
    db_session.commit()

    # Act
    result = repository.get_event_not_in_timeslot()

    # Assert
    titles = [it.title for it in result]
    assert "No Slot" in titles
    assert "With Slot" not in titles
