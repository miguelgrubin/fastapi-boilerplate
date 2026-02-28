from unittest.mock import patch

import pytest
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.domain.errors.user_not_found import UserNotFound
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.comment_repository_memory import CommentRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.comment_creator import CommentCreator
from src.blog.use_cases.user_creator import UserCreator
from src.shared.infrastructure.services.password_service_fake import PasswordServiceFake


def _create_repositories():
    article_repo = ArticleRepositoryMemory()
    article_repo.clear()
    comment_repo = CommentRepositoryMemory()
    comment_repo.clear()
    user_repo = UserRepositoryMemory()
    user_repo.clear()
    return article_repo, comment_repo, user_repo


def _create_user(user_repo):
    password_service = PasswordServiceFake()
    return UserCreator(user_repo, password_service).execute(
        "author", "S3CUR€ PA$$", "author@example.com"
    )


def _create_article(article_repo, user_repo, user):
    creator = ArticleCreator(article_repo, user_repo)
    return creator.execute(
        title="Test Article",
        description="Summary",
        content="Content",
        author_id=user.id,
    )


def test_should_create_comment_when_article_and_author_exist():
    article_repo, comment_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    article = _create_article(article_repo, user_repo, user)
    use_case = CommentCreator(comment_repo, article_repo, user_repo)

    comment = use_case.execute(
        content="Great article!",
        author_id=user.id,
        article_id=article.id,
    )

    assert comment.id != ""
    assert comment.content == "Great article!"
    assert comment.author_id == user.id
    assert comment.article_id == article.id
    assert comment.created_at is not None


def test_should_raise_error_when_article_not_found():
    article_repo, comment_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    use_case = CommentCreator(comment_repo, article_repo, user_repo)

    with pytest.raises(ArticleNotFound):
        use_case.execute(
            content="Comment",
            author_id=user.id,
            article_id="non-existent-article-id",
        )


def test_should_raise_error_when_author_not_found():
    article_repo, comment_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    article = _create_article(article_repo, user_repo, user)
    use_case = CommentCreator(comment_repo, article_repo, user_repo)

    with pytest.raises(UserNotFound):
        use_case.execute(
            content="Comment",
            author_id="non-existent-author-id",
            article_id=article.id,
        )


@patch.object(CommentRepositoryMemory, "save")
def test_should_save_on_repository(mock_save):
    article_repo, comment_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    article = _create_article(article_repo, user_repo, user)
    use_case = CommentCreator(comment_repo, article_repo, user_repo)

    use_case.execute(
        content="Comment",
        author_id=user.id,
        article_id=article.id,
    )

    mock_save.assert_called()


def test_should_record_comment_created_event():
    article_repo, comment_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    article = _create_article(article_repo, user_repo, user)
    use_case = CommentCreator(comment_repo, article_repo, user_repo)

    comment = use_case.execute(
        content="Comment",
        author_id=user.id,
        article_id=article.id,
    )

    events = comment.pull_domain_events()
    assert len(events) == 1
    assert events[0].event_type == "CommentCreatedEvent"
