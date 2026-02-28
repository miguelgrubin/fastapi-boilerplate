from unittest.mock import patch

import pytest
from src.blog.domain.errors.user_not_found import UserNotFound
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.user_creator import UserCreator
from src.shared.infrastructure.services.password_service_fake import PasswordServiceFake


def _create_repositories():
    article_repo = ArticleRepositoryMemory()
    article_repo.clear()
    user_repo = UserRepositoryMemory()
    user_repo.clear()
    return article_repo, user_repo


def _create_user(user_repo: UserRepositoryMemory):
    password_service = PasswordServiceFake()
    creator = UserCreator(user_repo, password_service)
    return creator.execute("author", "S3CUR€ PA$$", "author@example.com")


def _create_use_case():
    article_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    use_case = ArticleCreator(article_repo, user_repo)
    return use_case, user


def test_should_create_article_when_author_exists():
    use_case, user = _create_use_case()
    article = use_case.execute(
        title="My First Post",
        description="A short summary",
        content="Full article content here.",
        author_id=user.id,
    )
    assert article.id != ""
    assert article.title == "My First Post"
    assert article.description == "A short summary"
    assert article.content == "Full article content here."
    assert article.slug == "my-first-post"
    assert article.author_id == user.id
    assert article.published is False
    assert article.created_at is not None


def test_should_generate_slug_from_title():
    use_case, user = _create_use_case()
    article = use_case.execute(
        title="My fav post",
        description="Summary",
        content="Content",
        author_id=user.id,
    )
    assert article.slug == "my-fav-post"


def test_should_raise_error_when_author_not_found():
    use_case, _ = _create_use_case()
    with pytest.raises(UserNotFound):
        use_case.execute(
            title="My Post",
            description="Summary",
            content="Content",
            author_id="non-existent-author-id",
        )


@patch.object(ArticleRepositoryMemory, "save")
def test_should_save_on_repository(mock_save):
    use_case, user = _create_use_case()
    use_case.execute(
        title="My Post",
        description="Summary",
        content="Content",
        author_id=user.id,
    )
    mock_save.assert_called()


def test_should_record_article_created_event():
    use_case, user = _create_use_case()
    article = use_case.execute(
        title="My Post",
        description="Summary",
        content="Content",
        author_id=user.id,
    )
    events = article.pull_domain_events()
    assert len(events) == 1
    assert events[0].event_type == "ArticleCreatedEvent"


def test_should_create_article_with_category_id():
    use_case, user = _create_use_case()
    article = use_case.execute(
        title="Categorized Post",
        description="Summary",
        content="Content",
        author_id=user.id,
        category_id="cat-123",
    )
    assert article.category_id == "cat-123"


def test_should_create_article_with_tags():
    use_case, user = _create_use_case()
    article = use_case.execute(
        title="Tagged Post",
        description="Summary",
        content="Content",
        author_id=user.id,
        tags=["tag-1", "tag-2", "tag-3"],
    )
    assert article.tags == ["tag-1", "tag-2", "tag-3"]


def test_should_create_article_with_empty_tags_by_default():
    use_case, user = _create_use_case()
    article = use_case.execute(
        title="No Tags Post",
        description="Summary",
        content="Content",
        author_id=user.id,
    )
    assert article.tags == []
    assert article.category_id is None
