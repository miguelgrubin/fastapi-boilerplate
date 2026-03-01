import pytest
from src.blog.domain.comment import Comment
from src.blog.domain.user import User
from src.blog.infrastructure.storage.comment_repository_sql import CommentRepositorySql
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
def user_repository(sql_service):
    return UserRepositorySql(sql_service)


@pytest.fixture
def repository(sql_service):
    return CommentRepositorySql(sql_service)


@pytest.fixture
def author(user_repository) -> User:
    """Create and persist an author user for foreign key constraints."""
    user = User.create(username="author", password="hashed_pw", email="author@example.com")
    user_repository.save(user)
    return user


def _create_comment(
    author_id: str,
    article_id: str = "article-1",
    content: str = "Great article!",
) -> Comment:
    return Comment.create(content=content, author_id=author_id, article_id=article_id)


def test_should_save_and_find_comment(repository, author):
    comment = _create_comment(author_id=author.id)
    repository.save(comment)

    found = repository.find_one(comment.id)

    assert found is not None
    assert found.id == comment.id
    assert found.content == comment.content
    assert found.author_id == comment.author_id
    assert found.article_id == comment.article_id


def test_should_find_by_article_id(repository, author):
    comment1 = _create_comment(author_id=author.id, article_id="article-1", content="First")
    comment2 = _create_comment(author_id=author.id, article_id="article-1", content="Second")
    comment3 = _create_comment(author_id=author.id, article_id="article-2", content="Other")
    repository.save(comment1)
    repository.save(comment2)
    repository.save(comment3)

    comments = repository.find_by_article_id("article-1")

    assert len(comments) == 2
    contents = {c.content for c in comments}
    assert contents == {"First", "Second"}


def test_should_return_none_when_comment_not_found(repository):
    assert repository.find_one("nonexistent-id") is None


def test_should_return_empty_list_when_no_comments_for_article(repository):
    comments = repository.find_by_article_id("nonexistent-article")
    assert comments == []


def test_should_delete_comment(repository, author):
    comment = _create_comment(author_id=author.id)
    repository.save(comment)

    repository.delete(comment.id)

    assert repository.find_one(comment.id) is None


def test_should_update_existing_comment(repository, author):
    comment = _create_comment(author_id=author.id, content="Original")
    repository.save(comment)

    comment.content = "Updated content"
    repository.save(comment)

    found = repository.find_one(comment.id)

    assert found is not None
    assert found.content == "Updated content"
