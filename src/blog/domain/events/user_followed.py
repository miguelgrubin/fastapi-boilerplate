from src.shared.domain.events.domain_event import DomainEvent

USER_FOLLOWED_EVENT = "UserFollowedEvent"


class UserFollowed(DomainEvent):
    def __init__(self, user_id: str, followed_id: str) -> None:
        super().__init__(USER_FOLLOWED_EVENT)
        self.user_id = user_id
        self.followed_id = followed_id
