from uuid import uuid4

import pytest

from miseventos.infrastructure.persistence.postgresql.implement.session_register_implement import (
    SessionRegisterImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.event_model import (
    Event as EventModel,
)
from miseventos.infrastructure.persistence.postgresql.models.session_model import (
    Session as SessionModel,
)
from miseventos.infrastructure.persistence.postgresql.models.session_registration_model import (
    SessionRegistration,
)
from miseventos.infrastructure.persistence.postgresql.models.user_model import (
    User as UserModel,
)
from miseventos.infrastructure.persistence.postgresql.schemas.session_register_schema import (
    SessionRegisterDeleteRequest,
    SessionRegisterRequest,
)


def test_add_session_register(db_session):
    # Arrange
    repository = SessionRegisterImplement(db_session)
    event = EventModel(title="E", description="D", status="PUBLISHED")
    session = SessionModel(title="S", description="D", event_id=uuid4()) # simplify event_id here
    user = UserModel(email="u@test.com", password_hash="p", role="assistant")
    db_session.add_all([event, session, user])
    db_session.commit()
    db_session.refresh(event)
    db_session.refresh(session)
    db_session.refresh(user)
    
    # We need to set session.event_id correctly to avoid foreign key issues if strict, 
    # but SQLite doesn't always enforce it unless told. 
    session.event_id = event.id
    db_session.commit()

    reg_req = SessionRegisterRequest(
        user_id=str(user.id),
        session_id=str(session.id),
        event_id=str(event.id)
    )

    # Act
    result = repository.add_session_register(reg_req)

    # Assert
    assert result is not None
    assert result.success is True
    assert db_session.query(SessionRegistration).count() == 1

def test_delete_session_register(db_session):
    # Arrange
    repository = SessionRegisterImplement(db_session)
    user_id = uuid4()
    reg = SessionRegistration(user_id=user_id, session_id=uuid4())
    db_session.add(reg)
    db_session.commit()
    db_session.refresh(reg)

    del_req = SessionRegisterDeleteRequest(
        id=str(reg.id),
        user_id=str(user_id)
    )

    # Act
    result = repository.delete_session_register(del_req)

    # Assert
    assert result.success is True
    assert db_session.query(SessionRegistration).filter_by(id=reg.id).first() is None
