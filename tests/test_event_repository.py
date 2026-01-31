from src.miseventos.infrastructure.persistence.postgresql.models.event_model import EventModel, TimeSlot
from src.miseventos.repositories.event_repository import EventRepository


def test_get_event_not_in_timeslot(db_session):
    # ---------- Arrange ----------
    event_without_slot = EventModel(
        id=1,
        title="Evento sin timeslot"
    )

    event_with_slot = EventModel(
        id=2,
        title="Evento con timeslot"
    )

    timeslot = TimeSlot(
        id=1,
        event_id=2
    )

    db_session.add_all([
        event_without_slot,
        event_with_slot,
        timeslot
    ])
    db_session.commit()

    repository = EventRepository(db_session)

    # ---------- Act ----------
    result = repository.get_event_not_in_timeslot()

    # ---------- Assert ----------
    assert len(result) == 1
    assert result[0].event_id == 1
    assert result[0].title == "Evento sin timeslot"
