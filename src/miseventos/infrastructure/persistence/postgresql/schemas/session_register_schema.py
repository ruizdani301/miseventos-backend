from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel


class SessionRegisterRequest(SQLModel):
    event_id: UUID | None = None
    session_id: UUID
    user_id: UUID | None = None

class registerResponse(SQLModel):
    id: Optional[str] | UUID = None
    event_id: UUID | None = None
    session_id: UUID | None = None
    number_registered: int | None = None
    message: Optional[str] = None
    success: bool | None = None

class SessionRegisterResponse(SQLModel):
    success: bool
    error_message: Optional[str] = None
    session_detail: registerResponse 

class SessionRegisterDeleteRequest(SQLModel):
    register_id: UUID
    user_id: UUID

class SessionDeleteResponse(SQLModel):
    id: Optional[str] | UUID = None
    success: bool
    error_message: Optional[str] = None