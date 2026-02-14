from src.shared.domain.events.domain_event import DomainEvent

USER_UPDATED_EVENT = "UserUpdatedEvent"


class UserUpdated(DomainEvent):
    def __init__(self, payload) -> None:
        super().__init__(USER_UPDATED_EVENT)
        self.payload = payload
