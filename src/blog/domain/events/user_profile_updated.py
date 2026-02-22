from typing import Dict

from src.shared.domain.events.domain_event import DomainEvent

USER_PROFILE_UPDATED_EVENT = "UserProfileUpdatedEvent"


class UserProfileUpdated(DomainEvent):
    def __init__(self, user_id: str, payload: Dict) -> None:
        super().__init__(USER_PROFILE_UPDATED_EVENT)
        self.user_id = user_id
        self.payload = payload
