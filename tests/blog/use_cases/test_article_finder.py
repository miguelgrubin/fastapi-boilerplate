import pytest
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.article_finder import ArticleFinder
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
        title="Test Article",
        description="Test summary",
        content="Test content",
        author_id=user.id,
    )


def test_should_find_article_by_id():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    finder = ArticleFinder(article_repo)

    found = finder.execute(article.id)

    assert found.id == article.id
    assert found.title == "Test Article"


def test_should_find_article_by_slug():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    finder = ArticleFinder(article_repo)

    found = finder.execute_by_slug("test-article")

    assert found.id == article.id
    assert found.slug == "test-article"


def test_should_raise_error_when_article_not_found_by_id():
    article_repo, _ = _create_repositories()
    finder = ArticleFinder(article_repo)

    with pytest.raises(ArticleNotFound):
        finder.execute("non-existent-id")


def test_should_raise_error_when_article_not_found_by_slug():
    article_repo, _ = _create_repositories()
    finder = ArticleFinder(article_repo)

    with pytest.raises(ArticleNotFound):
        finder.execute_by_slug("non-existent-slug")
