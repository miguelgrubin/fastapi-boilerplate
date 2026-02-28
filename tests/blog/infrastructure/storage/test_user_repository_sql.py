import pytest
from src.blog.domain.user import User
from src.blog.infrastructure.storage.sql_tables import metadata
from src.blog.infrastructure.storage.user_repository_sql import UserRepositorySql
from src.shared.infrastructure.services.sql_service_sqlalchemy import SqlServiceSqlAlchemy


@pytest.fixture
def sql_service():
    """Create a SqlService backed by an in-memory SQLite database."""
    service = SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)
    service.connect()
    metadata.create_all(service._engine)
    yield service
    service.disconnect()


@pytest.fixture
def repository(sql_service):
    return UserRepositorySql(sql_service)


def _create_user(
    username: str = "someone",
    email: str = "someone@example.com",
) -> User:
    return User.create(username=username, password="hashed_pw", email=email)


def test_should_save_and_find_user(repository):
    user = _create_user()
    repository.save(user)

    found = repository.find_one(user.id)

    assert found is not None
    assert found.id == user.id
    assert found.email == user.email
    assert found.username == user.username
    assert found.password_hash == user.password_hash


def test_should_find_by_username(repository):
    user = _create_user(username="johndoe")
    repository.save(user)

    found = repository.find_one_by_username("johndoe")

    assert found is not None
    assert found.username == "johndoe"


def test_should_find_by_email(repository):
    user = _create_user(email="john@example.com")
    repository.save(user)

    found = repository.find_one_by_email("john@example.com")

    assert found is not None
    assert found.email == "john@example.com"


def test_should_return_none_when_user_not_found(repository):
    assert repository.find_one("nonexistent-id") is None
    assert repository.find_one_by_username("nonexistent") is None
    assert repository.find_one_by_email("nonexistent@example.com") is None


def test_should_delete_user(repository):
    user = _create_user()
    repository.save(user)

    repository.delete(user.id)

    assert repository.find_one(user.id) is None


def test_should_update_existing_user(repository):
    user = _create_user()
    repository.save(user)

    user.update_profile({"bio": "Hello world", "image": "https://img.com/me.png"})
    repository.save(user)

    found = repository.find_one(user.id)

    assert found is not None
    assert found.profile.bio == "Hello world"
    assert found.profile.image == "https://img.com/me.png"


def test_should_persist_following_and_followers(repository):
    user = _create_user()
    user.following = ["user-2", "user-3"]
    user.followers = ["user-4"]
    repository.save(user)

    found = repository.find_one(user.id)

    assert found is not None
    assert found.following == ["user-2", "user-3"]
    assert found.followers == ["user-4"]


def test_should_find_all_users(repository):
    user1 = _create_user(username="alice", email="alice@example.com")
    user2 = _create_user(username="bob", email="bob@example.com")
    repository.save(user1)
    repository.save(user2)

    users = repository.find_all(find_filters={}, find_order={}, find_limits=(0, 10))

    assert len(users) == 2
    usernames = {u.username for u in users}
    assert usernames == {"alice", "bob"}


def test_should_apply_offset_and_limit(repository):
    for i in range(5):
        user = _create_user(username=f"user{i}", email=f"user{i}@example.com")
        repository.save(user)

    users = repository.find_all(find_filters={}, find_order={}, find_limits=(2, 2))

    assert len(users) == 2
