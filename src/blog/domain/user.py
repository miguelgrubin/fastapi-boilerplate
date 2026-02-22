"""User Domain"""

from typing import List, Optional, TypedDict

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from src.blog.domain.errors.user_not_following import UserNotFollowing
from src.blog.domain.events.user_created import UserCreated
from src.blog.domain.events.user_followed import UserFollowed
from src.blog.domain.events.user_profile_updated import UserProfileUpdated
from src.blog.domain.events.user_unfollowed import UserUnfollowed
from src.shared.domain.domain_model import DomainModel


class UserProfileUpdateParams(TypedDict):
    bio: Optional[str]
    image: Optional[str]


@dataclass
class Profile:
    bio: Optional[str] = None
    image: Optional[str] = None


@dataclass
class User(DomainModel):
    """User from blog (writer)"""

    id: str
    email: str
    username: str
    password_hash: str
    updated_at: datetime
    created_at: datetime
    profile: Profile = field(default_factory=Profile)
    following: List[str] = field(default_factory=list)
    followers: List[str] = field(default_factory=list)

    @classmethod
    def create(cls, username: str, password: str, email: str) -> "User":
        """Creates a new User."""
        id = str(uuid4())
        now = datetime.now()

        user = User(
            id=id,
            email=email,
            username=username,
            password_hash=password,
            profile=Profile(),
            created_at=now,
            updated_at=now,
        )
        user.record(UserCreated(user.id))

        return user

    def update_profile(self, payload: UserProfileUpdateParams) -> None:
        """Updates email and profile info."""
        self.profile.bio = payload.get("bio", self.profile.bio)
        self.profile.image = payload.get("image", self.profile.image)
        self.updated_at = datetime.now()
        self.record(UserProfileUpdated(self.id, dict(payload)))

    def follow(self, user_id: str) -> None:
        self.following.append(user_id)
        self.record(UserFollowed(self.id, user_id))

    def unfollow(self, user_id: str) -> None:
        if user_id not in self.following:
            raise UserNotFollowing(user_id)
        self.following.remove(user_id)
        self.record(UserUnfollowed(self.id, user_id))
