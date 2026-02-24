from unittest.mock import patch

import pytest
from src.blog.domain.errors.comment_not_found import CommentNotFound
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.comment_repository_memory import CommentRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.comment_creator import CommentCreator
from src.blog.use_cases.comment_deleter import CommentDeleter
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


def _create_comment(article_repo, comment_repo, user_repo):
    password_service = PasswordServiceFake()
    user = UserCreator(user_repo, password_service).execute(
        "author", "S3CUR€ PA$$", "author@example.com"
    )
    article = ArticleCreator(article_repo, user_repo).execute(
        title="Test",
        description="Summary",
        content="Content",
        slug="test",
        author_id=user.id,
    )
    creator = CommentCreator(comment_repo, article_repo, user_repo)
    return creator.execute("A comment", user.id, article.id)


def test_should_delete_comment_when_it_exists():
    article_repo, comment_repo, user_repo = _create_repositories()
    comment = _create_comment(article_repo, comment_repo, user_repo)
    deleter = CommentDeleter(comment_repo)

    result = deleter.execute(comment.id)

    assert result is None
    assert comment_repo.find_one(comment.id) is None


def test_should_raise_error_when_comment_not_found():
    _, comment_repo, _ = _create_repositories()
    deleter = CommentDeleter(comment_repo)

    with pytest.raises(CommentNotFound):
        deleter.execute("non-existent-id")


@patch.object(CommentRepositoryMemory, "delete")
def test_should_call_delete_on_repository(mock_delete):
    article_repo, comment_repo, user_repo = _create_repositories()
    comment = _create_comment(article_repo, comment_repo, user_repo)
    deleter = CommentDeleter(comment_repo)

    deleter.execute(comment.id)

    mock_delete.assert_called_with(comment.id)
