from src.shared.domain.events.domain_event import DomainEvent

USER_CREATED_EVENT = "UserCreatedEvent"


class UserCreated(DomainEvent):
    def __init__(self, user_id: str) -> None:
        super().__init__(USER_CREATED_EVENT)
        self.user_id = user_id
