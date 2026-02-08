from uuid import UUID

import pytest

from miseventos.entitis.user import UserEntity
from miseventos.infrastructure.persistence.postgresql.implement.user_implement import (
    UserImplement,
)
from miseventos.infrastructure.persistence.postgresql.models.enum import RoleName
from miseventos.infrastructure.persistence.postgresql.models.user_model import (
    User as UserModel,
)


def test_add_user_success(db_session):
    # Arrange
    repository = UserImplement(db_session)
    user_entity = UserEntity(
        email="test@example.com",
        password="hashed_password",
        role=RoleName.ASSISTANT.value
    )

    # Act
    result = repository.add_user(user_entity)

    # Assert
    assert result.email == "test@example.com"
    assert result.id is not None
    
    db_user = db_session.query(UserModel).filter_by(email="test@example.com").first()
    assert db_user is not None
    assert db_user.password_hash == "hashed_password"

def test_get_users(db_session):
    # Arrange
    repository = UserImplement(db_session)
    user1 = UserModel(email="user1@example.com", password_hash="pass1", role=RoleName.ASSISTANT.value)
    user2 = UserModel(email="user2@example.com", password_hash="pass2", role=RoleName.ASSISTANT.value)
    db_session.add_all([user1, user2])
    db_session.commit()

    # Act
    users = repository.get_users()

    # Assert
    assert len(users) == 2
    emails = [u.email for u in users]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails

def test_get_user_by_id(db_session):
    # Arrange
    repository = UserImplement(db_session)
    db_user = UserModel(email="findme@example.com", password_hash="pass", role=RoleName.ASSISTANT.value)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)

    # Act
    result = repository.get_user_by_id(db_user.id)

    # Assert
    assert result is not None
    assert result.email == "findme@example.com"
    assert result.id == db_user.id

def test_get_user_by_email(db_session):
    # Arrange
    repository = UserImplement(db_session)
    db_user = UserModel(email="email@example.com", password_hash="pass", role=RoleName.ASSISTANT.value)
    db_session.add(db_user)
    db_session.commit()

    # Act
    result = repository.get_user_by_email("email@example.com")

    # Assert
    assert result is not None
    assert result.email == "email@example.com"

def test_update_user(db_session):
    # Arrange
    repository = UserImplement(db_session)
    db_user = UserModel(email="old@example.com", password_hash="oldpass", role=RoleName.ASSISTANT.value)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)

    update_entity = UserEntity(
        id=db_user.id,
        email="new@example.com",
        password="newpass",
        role=RoleName.ASSISTANT.value
    )

    # Act
    result = repository.update_user(update_entity)

    # Assert
    assert result is not None
    assert result.email == "new@example.com"
    
    db_user_updated = db_session.query(UserModel).filter_by(id=db_user.id).first()
    assert db_user_updated.email == "new@example.com"
    assert db_user_updated.password_hash == "newpass"

def test_delete_user(db_session):
    # Arrange
    repository = UserImplement(db_session)
    db_user = UserModel(email="delete@example.com", password_hash="pass", role=RoleName.ASSISTANT.value)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)

    # Act
    result = repository.delete_user(db_user.id)

    # Assert
    assert result is not None
    assert result.id == db_user.id
    
    db_user_after = db_session.query(UserModel).filter_by(id=db_user.id).first()
    assert db_user_after is None
