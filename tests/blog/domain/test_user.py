import pytest
from src.blog.domain.errors.user_not_following import UserNotFollowing
from src.blog.domain.events.user_created import USER_CREATED_EVENT, UserCreated
from src.blog.domain.events.user_followed import USER_FOLLOWED_EVENT, UserFollowed
from src.blog.domain.events.user_profile_updated import (
    USER_PROFILE_UPDATED_EVENT,
    UserProfileUpdated,
)
from src.blog.domain.events.user_unfollowed import USER_UNFOLLOWED_EVENT, UserUnfollowed
from src.blog.domain.user import Profile, User


def _create_user(**overrides):
    defaults = {
        "username": "testuser",
        "password": "hashed_pw",
        "email": "test@example.com",
    }
    defaults.update(overrides)
    return User.create(**defaults)


def test_should_create_user_with_valid_fields():
    user = _create_user()
    assert user.id != ""
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password_hash == "hashed_pw"
    assert user.created_at is not None
    assert user.updated_at is not None


def test_should_create_user_with_default_profile():
    user = _create_user()
    assert isinstance(user.profile, Profile)
    assert user.profile.bio is None
    assert user.profile.image is None


def test_should_create_user_with_empty_following_and_followers():
    user = _create_user()
    assert user.following == []
    assert user.followers == []


def test_should_record_user_created_event():
    user = _create_user()
    events = user.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], UserCreated)
    assert events[0].user_id == user.id
    assert events[0].event_type == USER_CREATED_EVENT


def test_should_update_profile_bio_and_image():
    user = _create_user()
    user.update_profile({"bio": "Hello world", "image": "https://img.png"})
    assert user.profile.bio == "Hello world"
    assert user.profile.image == "https://img.png"


def test_should_keep_existing_profile_values_when_not_provided():
    user = _create_user()
    user.update_profile({"bio": "Original bio", "image": "original.png"})
    user.update_profile({"bio": "New bio"})
    assert user.profile.bio == "New bio"
    assert user.profile.image == "original.png"


def test_should_record_user_profile_updated_event():
    user = _create_user()
    user.pull_domain_events()
    payload = {"bio": "Updated", "image": None}
    user.update_profile(payload)
    events = user.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], UserProfileUpdated)
    assert events[0].user_id == user.id
    assert events[0].event_type == USER_PROFILE_UPDATED_EVENT


def test_should_follow_user():
    user = _create_user()
    user.follow("other-user-123")
    assert "other-user-123" in user.following


def test_should_record_user_followed_event():
    user = _create_user()
    user.pull_domain_events()
    user.follow("other-user-123")
    events = user.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], UserFollowed)
    assert events[0].user_id == user.id
    assert events[0].followed_id == "other-user-123"
    assert events[0].event_type == USER_FOLLOWED_EVENT


def test_should_unfollow_user():
    user = _create_user()
    user.follow("other-user-123")
    user.unfollow("other-user-123")
    assert "other-user-123" not in user.following


def test_should_record_user_unfollowed_event():
    user = _create_user()
    user.follow("other-user-123")
    user.pull_domain_events()
    user.unfollow("other-user-123")
    events = user.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], UserUnfollowed)
    assert events[0].user_id == user.id
    assert events[0].unfollowed_id == "other-user-123"
    assert events[0].event_type == USER_UNFOLLOWED_EVENT


def test_should_raise_user_not_following_when_unfollowing_unknown_user():
    user = _create_user()
    with pytest.raises(UserNotFollowing):
        user.unfollow("unknown-user-id")
