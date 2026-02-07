import uuid
from abc import ABC

from app.shared.domain.events.event_types import EventType


class DomainEvent(ABC):
    id: str
    event_type: EventType

    def __init__(self, event_type: EventType) -> None:
        self.id = str(uuid.uuid4())
        self.event_type = event_type
        super().__init__()
