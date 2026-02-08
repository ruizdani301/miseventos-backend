from uuid import uuid4

import pytest

from miseventos.entitis.speaker import SpeakerEntity
from miseventos.infrastructure.persistence.postgresql.implement.speaker_implement import (
    SpeakerImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.event_model import (
    Event as EventModel,
)
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session as SessionModel,
)
from miseventos.infrastructure.persistence.postgresql.models.session_speaker_model import (
    SessionSpeaker,
)
from miseventos.infrastructure.persistence.postgresql.models.speaker_model import (
    Speaker as SpeakerModel,
)
from miseventos.infrastructure.persistence.postgresql.schemas.speaker_schema import (
    SpeakerUpdateRequest,
)


def test_add_speaker(db_session):
    # Arrange
    repository = SpeakerImplement(db_session)
    speaker_entity = SpeakerEntity(
        full_name="John Doe",
        email="john@example.com",
        bio="Test Bio"
    )

    # Act
    result = repository.add_speaker(speaker_entity)

    # Assert
    assert result.id is not None
    db_speaker = db_session.query(SpeakerModel).filter_by(email="john@example.com").first()
    assert db_speaker is not None
    assert db_speaker.full_name == "John Doe"

def test_get_speakers(db_session):
    # Arrange
    repository = SpeakerImplement(db_session)
    s1 = SpeakerModel(full_name="A", email="a@test.com", bio="bio")
    s2 = SpeakerModel(full_name="B", email="b@test.com", bio="bio")
    db_session.add_all([s1, s2])
    db_session.commit()

    # Act
    result = repository.get_speaker()

    # Assert
    assert len(result) == 2
    # In SpeakerImplement.get_speaker, it orders by full_name desc
    assert result[0].full_name == "B"
    assert result[1].full_name == "A"

def test_update_speaker(db_session):
    # Arrange
    repository = SpeakerImplement(db_session)
    db_speaker = SpeakerModel(full_name="Old Name", email="old@test.com", bio="old bio")
    db_session.add(db_speaker)
    db_session.commit()
    db_session.refresh(db_speaker)

    update_request = SpeakerUpdateRequest(
        id=db_speaker.id,
        full_name="New Name",
        email="new@test.com",
        bio="new bio"
    )

    # Act
    result = repository.update_speaker(update_request)

    # Assert
    assert result.full_name == "New Name"
    assert result.email == "new@test.com"

def test_delete_speaker(db_session):
    # Arrange
    repository = SpeakerImplement(db_session)
    db_speaker = SpeakerModel(full_name="Delete Me", email="del@test.com", bio="bio")
    db_session.add(db_speaker)
    db_session.commit()
    db_session.refresh(db_speaker)

    # Act
    result = repository.delete_speaker(db_speaker.id)

    # Assert
    assert result == db_speaker.id
    assert db_session.query(SpeakerModel).filter_by(id=db_speaker.id).first() is None

def test_get_speaker_by_event_id(db_session):
    # Arrange
    repository = SpeakerImplement(db_session)
    event = EventModel(title="Test Event", description="Desc", status="PUBLISHED")
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    speaker = SpeakerModel(full_name="Speaker 1", email="s1@test.com", bio="bio")
    db_session.add(speaker)
    db_session.commit()
    db_session.refresh(speaker)

    session = SessionModel(title="Session 1", description="Desc", event_id=event.id)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    assoc = SessionSpeaker(session_id=session.id, speaker_id=speaker.id)
    db_session.add(assoc)
    db_session.commit()

    # Act
    result = repository.get_speaker_by_event_id(event.id)

    # Assert
    assert len(result) == 1
    assert result[0].full_name == "Speaker 1"
