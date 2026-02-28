import uuid

from src.blog.domain.events.article_created import ArticleCreated, ARTICLE_CREATED_EVENT
from src.blog.domain.events.article_published import ArticlePublished, ARTICLE_PUBLISHED_EVENT
from src.blog.domain.events.article_unpublished import (
    ArticleUnpublished,
    ARTICLE_UNPUBLISHED_EVENT,
)
from src.blog.domain.events.article_updated import ArticleUpdated, ARTICLE_UPDATED_EVENT
from src.blog.domain.events.comment_created import CommentCreated, COMMENT_CREATED_EVENT
from src.blog.domain.events.comment_deleted import CommentDeleted, COMMENT_DELETED_EVENT
from src.blog.domain.events.user_created import UserCreated, USER_CREATED_EVENT
from src.blog.domain.events.user_deleted import UserDeleted, USER_DELETED_EVENT
from src.blog.domain.events.user_followed import UserFollowed, USER_FOLLOWED_EVENT
from src.blog.domain.events.user_profile_updated import (
    UserProfileUpdated,
    USER_PROFILE_UPDATED_EVENT,
)
from src.blog.domain.events.user_unfollowed import UserUnfollowed, USER_UNFOLLOWED_EVENT


def _assert_valid_uuid(value: str) -> None:
    parsed = uuid.UUID(value)
    assert str(parsed) == value


def test_article_created_event():
    event = ArticleCreated("art-1")
    assert event.event_type == ARTICLE_CREATED_EVENT
    assert event.article_id == "art-1"
    _assert_valid_uuid(event.id)


def test_article_published_event():
    event = ArticlePublished("art-2")
    assert event.event_type == ARTICLE_PUBLISHED_EVENT
    assert event.article_id == "art-2"
    _assert_valid_uuid(event.id)


def test_article_unpublished_event():
    event = ArticleUnpublished("art-3")
    assert event.event_type == ARTICLE_UNPUBLISHED_EVENT
    assert event.article_id == "art-3"
    _assert_valid_uuid(event.id)


def test_article_updated_event():
    payload = {"title": "New Title"}
    event = ArticleUpdated("art-4", payload)
    assert event.event_type == ARTICLE_UPDATED_EVENT
    assert event.article_id == "art-4"
    assert event.payload == {"title": "New Title"}
    _assert_valid_uuid(event.id)


def test_user_created_event():
    event = UserCreated("user-1")
    assert event.event_type == USER_CREATED_EVENT
    assert event.user_id == "user-1"
    _assert_valid_uuid(event.id)


def test_user_deleted_event():
    event = UserDeleted("user-2")
    assert event.event_type == USER_DELETED_EVENT
    assert event.user_id == "user-2"
    _assert_valid_uuid(event.id)


def test_user_followed_event():
    event = UserFollowed("user-3", "user-4")
    assert event.event_type == USER_FOLLOWED_EVENT
    assert event.user_id == "user-3"
    assert event.followed_id == "user-4"
    _assert_valid_uuid(event.id)


def test_user_unfollowed_event():
    event = UserUnfollowed("user-5", "user-6")
    assert event.event_type == USER_UNFOLLOWED_EVENT
    assert event.user_id == "user-5"
    assert event.unfollowed_id == "user-6"
    _assert_valid_uuid(event.id)


def test_user_profile_updated_event():
    payload = {"bio": "New bio"}
    event = UserProfileUpdated("user-7", payload)
    assert event.event_type == USER_PROFILE_UPDATED_EVENT
    assert event.user_id == "user-7"
    assert event.payload == {"bio": "New bio"}
    _assert_valid_uuid(event.id)


def test_comment_created_event():
    event = CommentCreated("com-1", "art-10")
    assert event.event_type == COMMENT_CREATED_EVENT
    assert event.comment_id == "com-1"
    assert event.article_id == "art-10"
    _assert_valid_uuid(event.id)


def test_comment_deleted_event():
    event = CommentDeleted("com-2", "art-11")
    assert event.event_type == COMMENT_DELETED_EVENT
    assert event.comment_id == "com-2"
    assert event.article_id == "art-11"
    _assert_valid_uuid(event.id)


def test_each_event_gets_unique_id():
    event_a = ArticleCreated("art-x")
    event_b = ArticleCreated("art-x")
    assert event_a.id != event_b.id
