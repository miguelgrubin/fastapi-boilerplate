import uuid
from abc import ABC


class DomainEvent(ABC):
    id: str
    event_type: str

    def __init__(self, event_type: str) -> None:
        self.id = str(uuid.uuid4())
        self.event_type = event_type
        super().__init__()
