"""User Domain"""

from typing import List, Optional, TypedDict

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from src.blog.domain.errors.user_not_following import UserNotFollowing
from src.blog.domain.events.user_created import UserCreated
from src.blog.domain.events.user_followed import UserFollowed
from src.blog.domain.events.user_unfollowed import UserUnfollowed
from src.blog.domain.events.user_updated import UserUpdated
from src.shared.domain.domain_model import DomainModel


class UserUpdateParams(TypedDict):
    bio: Optional[str]
    image: Optional[str]


@dataclass
class Profile:
    bio: Optional[str] = None
    image: Optional[str] = None


class User(DomainModel):
    """User from blog (writer)"""

    id: str
    email: str
    username: str
    password_hash: str
    profile: Profile
    following: List[str] = field(default_factory=list)
    followers: List[str] = field(default_factory=list)
    updated_at: datetime
    created_at: datetime

    @classmethod
    def create(cls, username: str, password: str, email: str):
        """Creates a new User."""
        user = User()
        user.id = str(uuid4())
        user.email = email
        user.username = username
        user.password_hash = password
        user.profile = Profile()
        user.updated_at = datetime.now()
        user.created_at = datetime.now()

        user.record(UserCreated())
        return user

    def update_profile(self, payload: UserUpdateParams):
        """Updates email and profile info."""
        self.profile.bio = payload.get("bio", self.profile.bio)
        self.profile.image = payload.get("image", self.profile.image)
        self.updated_at = datetime.now()
        self.record(UserUpdated(payload))

    def follow(self, user_id: str):
        self.following.append(user_id)
        self.record(UserFollowed(user_id))

    def unfollow(self, user_id: str):
        if user_id not in self.following:
            raise UserNotFollowing(user_id)
        self.following.remove(user_id)
        self.record(UserUnfollowed(user_id))
