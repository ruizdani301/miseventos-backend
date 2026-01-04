
import enum

class EventStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    closed = "closed"
