import pytest
from src.blog.domain.category import Category
from src.blog.infrastructure.storage.category_repository_sql import CategoryRepositorySql
from src.blog.infrastructure.storage.sql_tables import metadata
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
    return CategoryRepositorySql(sql_service)


def _create_category(name: str = "Technology") -> Category:
    return Category.create(name=name)


def test_should_save_and_find_category(repository):
    category = _create_category()
    repository.save(category)

    found = repository.find_one(category.id)

    assert found is not None
    assert found.id == category.id
    assert found.name == category.name
    assert found.slug == category.slug


def test_should_find_by_slug(repository):
    category = _create_category(name="Web Development")
    repository.save(category)

    found = repository.find_by_slug("web-development")

    assert found is not None
    assert found.name == "Web Development"
    assert found.slug == "web-development"


def test_should_return_none_when_category_not_found(repository):
    assert repository.find_one("nonexistent-id") is None
    assert repository.find_by_slug("nonexistent") is None


def test_should_find_all_categories(repository):
    cat1 = _create_category(name="Technology")
    cat2 = _create_category(name="Science")
    repository.save(cat1)
    repository.save(cat2)

    categories = repository.find_all()

    assert len(categories) == 2
    names = {c.name for c in categories}
    assert names == {"Technology", "Science"}


def test_should_update_existing_category(repository):
    category = _create_category(name="Tecnology")
    repository.save(category)

    category.name = "Technology"
    category.slug = "technology"
    repository.save(category)

    found = repository.find_one(category.id)

    assert found is not None
    assert found.name == "Technology"
    assert found.slug == "technology"
