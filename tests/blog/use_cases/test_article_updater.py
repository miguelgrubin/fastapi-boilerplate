from unittest.mock import patch

import pytest
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.article_updater import ArticleUpdater
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
        title="Original Title",
        description="Original Summary",
        content="Original Content",
        slug="original-title",
        author_id=user.id,
    )


def test_should_update_article_title():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    updater = ArticleUpdater(article_repo)

    updated = updater.execute(article.id, {"title": "Updated Title"})

    assert updated.title == "Updated Title"
    assert updated.description == "Original Summary"


def test_should_update_multiple_fields():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    updater = ArticleUpdater(article_repo)

    updated = updater.execute(
        article.id,
        {
            "title": "New Title",
            "content": "New Content",
            "slug": "new-title",
        },
    )

    assert updated.title == "New Title"
    assert updated.content == "New Content"
    assert updated.slug == "new-title"


def test_should_raise_error_when_article_not_found():
    article_repo, _ = _create_repositories()
    updater = ArticleUpdater(article_repo)

    with pytest.raises(ArticleNotFound):
        updater.execute("non-existent-id", {"title": "Updated"})


def test_should_update_updated_at_timestamp():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    original_updated_at = article.updated_at
    updater = ArticleUpdater(article_repo)

    updated = updater.execute(article.id, {"title": "Updated Title"})

    assert updated.updated_at >= original_updated_at


def test_should_save_on_repository():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    updater = ArticleUpdater(article_repo)

    with patch.object(article_repo, "save") as mock_save:
        updater.execute(article.id, {"title": "Updated"})
        mock_save.assert_called()


def test_should_update_category_id():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    updater = ArticleUpdater(article_repo)

    updated = updater.execute(article.id, {"category_id": "cat-456"})

    assert updated.category_id == "cat-456"


def test_should_update_tags():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    updater = ArticleUpdater(article_repo)

    updated = updater.execute(article.id, {"tags": ["tag-a", "tag-b"]})

    assert updated.tags == ["tag-a", "tag-b"]


def test_should_clear_category_id():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    updater = ArticleUpdater(article_repo)

    updater.execute(article.id, {"category_id": "cat-123"})
    updated = updater.execute(article.id, {"category_id": None})

    assert updated.category_id is None
