from src.shared.domain.events.domain_event import DomainEvent

USER_CREATED_EVENT = "UserCreatedEvent"


class UserCreated(DomainEvent):
    def __init__(self) -> None:
        super().__init__(USER_CREATED_EVENT)
