from uuid import uuid4

import pytest

from miseventos.infrastructure.persistence.postgresql.implement.session_implement import (
    SessionImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.event_model import (
    Event as EventModel,
)
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session as SessionModel,
)
from miseventos.infrastructure.persistence.postgresql.models.speaker_model import (
    Speaker as SpeakerModel,
)
from miseventos.infrastructure.persistence.postgresql.schemas.session_schema import (
    SessionRequest,
    SessionUpdateRequest,
)


def test_add_session(db_session):
    # Arrange
    repository = SessionImplement(db_session)
    event = EventModel(title="E", description="D", status="PUBLISHED")
    speaker = SpeakerModel(full_name="S", email="s@test.com", bio="B")
    db_session.add_all([event, speaker])
    db_session.commit()
    db_session.refresh(event)
    db_session.refresh(speaker)

    session_req = SessionRequest(
        title="Session 1",
        description="Desc",
        event_id=str(event.id),
        speaker_id=str(speaker.id),
        start_time="2023-10-01T10:00:00",
        end_time="2023-10-01T11:00:00"
    )

    # Act
    result = repository.add_session(session_req)

    # Assert
    assert result.title == "Session 1"
    assert db_session.query(SessionModel).count() == 1

def test_get_session_by_event_id(db_session):
    # Arrange
    repository = SessionImplement(db_session)
    event_id = uuid4()
    session = SessionModel(title="S", description="D", event_id=event_id)
    db_session.add(session)
    db_session.commit()

    # Act
    result = repository.get_session_by_event_id(event_id)

    # Assert
    assert len(result) == 1
    assert result[0].title == "S"

def test_delete_session(db_session):
    # Arrange
    repository = SessionImplement(db_session)
    session = SessionModel(title="S", description="D", event_id=uuid4())
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    # Act
    result = repository.delete_session(session.id)

    # Assert
    assert result == str(session.id)
    assert db_session.query(SessionModel).filter_by(id=session.id).first() is None
