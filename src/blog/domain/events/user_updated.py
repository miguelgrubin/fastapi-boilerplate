from src.shared.domain.events.domain_event import DomainEvent

USER_UPDATED_EVENT = "UserUpdatedEvent"


class UserUpdated(DomainEvent):
    def __init__(self, user_id: str, payload) -> None:
        super().__init__(USER_UPDATED_EVENT)
        self.user_id = user_id
        self.payload = payload
