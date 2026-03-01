import pytest
from src.blog.domain.tag import Tag
from src.blog.infrastructure.storage.sql_tables import metadata
from src.blog.infrastructure.storage.tag_repository_sql import TagRepositorySql
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
    return TagRepositorySql(sql_service)


def _create_tag(name: str = "Python") -> Tag:
    return Tag.create(name=name)


def test_should_save_and_find_tag(repository):
    tag = _create_tag()
    repository.save(tag)

    found = repository.find_one(tag.id)

    assert found is not None
    assert found.id == tag.id
    assert found.name == tag.name
    assert found.slug == tag.slug


def test_should_find_by_slug(repository):
    tag = _create_tag(name="Machine Learning")
    repository.save(tag)

    found = repository.find_by_slug("machine-learning")

    assert found is not None
    assert found.name == "Machine Learning"
    assert found.slug == "machine-learning"


def test_should_return_none_when_tag_not_found(repository):
    assert repository.find_one("nonexistent-id") is None
    assert repository.find_by_slug("nonexistent") is None


def test_should_find_all_tags(repository):
    tag1 = _create_tag(name="Python")
    tag2 = _create_tag(name="FastAPI")
    repository.save(tag1)
    repository.save(tag2)

    tags = repository.find_all()

    assert len(tags) == 2
    names = {t.name for t in tags}
    assert names == {"Python", "FastAPI"}


def test_should_update_existing_tag(repository):
    tag = _create_tag(name="Pytohn")
    repository.save(tag)

    tag.name = "Python"
    tag.slug = "python"
    repository.save(tag)

    found = repository.find_one(tag.id)

    assert found is not None
    assert found.name == "Python"
    assert found.slug == "python"
