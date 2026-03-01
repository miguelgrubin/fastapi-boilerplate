import pytest
from src.blog.domain.article import Article
from src.blog.domain.tag import Tag
from src.blog.domain.user import User
from src.blog.infrastructure.storage.article_repository_sql import ArticleRepositorySql
from src.blog.infrastructure.storage.sql_tables import metadata
from src.blog.infrastructure.storage.tag_repository_sql import TagRepositorySql
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
def user_repository(sql_service):
    return UserRepositorySql(sql_service)


@pytest.fixture
def tag_repository(sql_service):
    return TagRepositorySql(sql_service)


@pytest.fixture
def repository(sql_service):
    return ArticleRepositorySql(sql_service)


@pytest.fixture
def author(user_repository) -> User:
    """Create and persist an author user for foreign key constraints."""
    user = User.create(username="author", password="hashed_pw", email="author@example.com")
    user_repository.save(user)
    return user


def _create_article(
    author_id: str,
    title: str = "My Article",
    tags: list | None = None,
    category_id: str | None = None,
) -> Article:
    return Article.create(
        title=title,
        description="A test article",
        content="Article body content",
        author_id=author_id,
        category_id=category_id,
        tags=tags or [],
    )


def test_should_save_and_find_article(repository, author):
    article = _create_article(author_id=author.id)
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert found.id == article.id
    assert found.title == article.title
    assert found.description == article.description
    assert found.content == article.content
    assert found.slug == article.slug
    assert found.author_id == author.id
    assert found.published is False


def test_should_find_by_slug(repository, author):
    article = _create_article(author_id=author.id, title="Hello World")
    repository.save(article)

    found = repository.find_by_slug("hello-world")

    assert found is not None
    assert found.title == "Hello World"
    assert found.slug == "hello-world"


def test_should_return_none_when_article_not_found(repository):
    assert repository.find_one("nonexistent-id") is None
    assert repository.find_by_slug("nonexistent") is None


def test_should_delete_article(repository, author):
    article = _create_article(author_id=author.id)
    repository.save(article)

    repository.delete(article.id)

    assert repository.find_one(article.id) is None


def test_should_update_existing_article(repository, author):
    article = _create_article(author_id=author.id)
    repository.save(article)

    article.update({"title": "Updated Title", "content": "New content"})
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert found.title == "Updated Title"
    assert found.content == "New content"
    assert found.slug == "updated-title"


def test_should_persist_publish_state(repository, author):
    article = _create_article(author_id=author.id)
    repository.save(article)

    article.publish()
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert found.published is True


def test_should_persist_tags(repository, tag_repository, author):
    tag1 = Tag.create(name="Python")
    tag2 = Tag.create(name="FastAPI")
    tag_repository.save(tag1)
    tag_repository.save(tag2)

    article = _create_article(author_id=author.id, tags=[tag1.id, tag2.id])
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert set(found.tags) == {tag1.id, tag2.id}


def test_should_update_tags(repository, tag_repository, author):
    tag1 = Tag.create(name="Python")
    tag2 = Tag.create(name="FastAPI")
    tag3 = Tag.create(name="SQLAlchemy")
    tag_repository.save(tag1)
    tag_repository.save(tag2)
    tag_repository.save(tag3)

    article = _create_article(author_id=author.id, tags=[tag1.id, tag2.id])
    repository.save(article)

    article.update({"tags": [tag2.id, tag3.id]})
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert set(found.tags) == {tag2.id, tag3.id}


def test_should_delete_article_with_tags(repository, tag_repository, author):
    tag = Tag.create(name="Python")
    tag_repository.save(tag)

    article = _create_article(author_id=author.id, tags=[tag.id])
    repository.save(article)

    repository.delete(article.id)

    assert repository.find_one(article.id) is None


def test_should_find_all_articles(repository, author):
    article1 = _create_article(author_id=author.id, title="First Post")
    article2 = _create_article(author_id=author.id, title="Second Post")
    repository.save(article1)
    repository.save(article2)

    articles = repository.find_all(find_filters={}, find_order={}, find_limits=(0, 10))

    assert len(articles) == 2
    titles = {a.title for a in articles}
    assert titles == {"First Post", "Second Post"}


def test_should_apply_offset_and_limit(repository, author):
    titles = ["Alpha Post", "Beta Post", "Gamma Post", "Delta Post", "Epsilon Post"]
    for title in titles:
        article = _create_article(author_id=author.id, title=title)
        repository.save(article)

    articles = repository.find_all(find_filters={}, find_order={}, find_limits=(2, 2))

    assert len(articles) == 2


def test_should_persist_category_id(repository, author):
    article = _create_article(author_id=author.id, category_id="cat-123")
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert found.category_id == "cat-123"
