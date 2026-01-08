from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SpeakerEntity:
    id: Optional[str] = None
    full_name: str = None
    email: str = None
    bio: str = None
    created_at: datetime = None
