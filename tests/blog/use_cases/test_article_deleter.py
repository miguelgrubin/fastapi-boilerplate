from unittest.mock import patch

import pytest
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.article_deleter import ArticleDeleter
from src.blog.use_cases.user_creator import UserCreator
from src.shared.infrastructure.services.password_service_fake import PasswordServiceFake


def _create_repositories():
    article_repo = ArticleRepositoryMemory()
    article_repo.clear()
    user_repo = UserRepositoryMemory()
    user_repo.clear()
    return article_repo, user_repo


def _create_article(article_repo, user_repo):
    password_service = PasswordServiceFake()
    user = UserCreator(user_repo, password_service).execute(
        "author", "S3CUR€ PA$$", "author@example.com"
    )
    creator = ArticleCreator(article_repo, user_repo)
    return creator.execute(
        title="To Be Deleted",
        description="Summary",
        content="Content",
        author_id=user.id,
    )


def test_should_delete_article_when_it_exists():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    deleter = ArticleDeleter(article_repo)

    result = deleter.execute(article.id)

    assert result is None
    assert article_repo.find_one(article.id) is None


def test_should_raise_error_when_article_not_found():
    article_repo, _ = _create_repositories()
    deleter = ArticleDeleter(article_repo)

    with pytest.raises(ArticleNotFound):
        deleter.execute("non-existent-id")


@patch.object(ArticleRepositoryMemory, "delete")
def test_should_call_delete_on_repository(mock_delete):
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    deleter = ArticleDeleter(article_repo)

    deleter.execute(article.id)

    mock_delete.assert_called_with(article.id)
