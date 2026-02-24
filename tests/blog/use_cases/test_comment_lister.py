import pytest
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.comment_repository_memory import CommentRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.comment_creator import CommentCreator
from src.blog.use_cases.comment_lister import CommentLister
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
        slug="test-article",
        author_id=user.id,
    )


def test_should_return_empty_list_when_no_comments():
    article_repo, comment_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    article = _create_article(article_repo, user_repo, user)
    lister = CommentLister(comment_repo, article_repo)

    comments = lister.execute(article.id)

    assert comments == []


def test_should_return_comments_for_article():
    article_repo, comment_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    article = _create_article(article_repo, user_repo, user)
    creator = CommentCreator(comment_repo, article_repo, user_repo)

    creator.execute("First comment", user.id, article.id)
    creator.execute("Second comment", user.id, article.id)

    lister = CommentLister(comment_repo, article_repo)
    comments = lister.execute(article.id)

    assert len(comments) == 2


def test_should_not_return_comments_from_other_articles():
    article_repo, comment_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    article1 = _create_article(article_repo, user_repo, user)

    article2 = ArticleCreator(article_repo, user_repo).execute(
        title="Other Article",
        description="Other",
        content="Other",
        slug="other-article",
        author_id=user.id,
    )

    creator = CommentCreator(comment_repo, article_repo, user_repo)
    creator.execute("Comment on article 1", user.id, article1.id)
    creator.execute("Comment on article 2", user.id, article2.id)

    lister = CommentLister(comment_repo, article_repo)
    comments = lister.execute(article1.id)

    assert len(comments) == 1
    assert comments[0].content == "Comment on article 1"


def test_should_raise_error_when_article_not_found():
    article_repo, comment_repo, _ = _create_repositories()
    lister = CommentLister(comment_repo, article_repo)

    with pytest.raises(ArticleNotFound):
        lister.execute("non-existent-article-id")
