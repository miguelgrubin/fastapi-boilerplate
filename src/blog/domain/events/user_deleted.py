from src.shared.domain.events.domain_event import DomainEvent

USER_DELETED_EVENT = "UserDeletedEvent"


class UserDeleted(DomainEvent):
    def __init__(self, user_id: str) -> None:
        super().__init__(USER_DELETED_EVENT)
        self.user_id = user_id
