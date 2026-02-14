from src.shared.domain.events.domain_event import DomainEvent

USER_UNFOLLOWED_EVENT = "UserUnfollowedEvent"


class UserUnfollowed(DomainEvent):
    def __init__(self, user_id: str, unfollowed_id: str) -> None:
        super().__init__(USER_UNFOLLOWED_EVENT)
        self.user_id = user_id
        self.unfollowed_id = unfollowed_id
