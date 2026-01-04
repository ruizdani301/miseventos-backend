from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .user_model import UserModel as User
from uuid import UUID, uuid4


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True
    )
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None

    users: List["User"] = Relationship(back_populates="role")
