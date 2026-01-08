import enum


class EventStatus(str, enum.Enum):
    PUBLISHED = "published"
    CLOSED = "closed"


class RoleName(str, enum.Enum):
    ADMIN = "admin"
    ASSISTANT = "assistant"

    @classmethod
    def values(cls):
        return [item.value for item in cls]
