import pytest
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.article_publisher import ArticlePublisher
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
        title="Draft Article",
        description="Summary",
        content="Content",
        author_id=user.id,
    )


def test_should_publish_article():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    publisher = ArticlePublisher(article_repo)

    published = publisher.execute(article.id)

    assert published.published is True


def test_should_unpublish_article():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    publisher = ArticlePublisher(article_repo)

    publisher.execute(article.id)
    unpublished = publisher.unpublish(article.id)

    assert unpublished.published is False


def test_should_raise_error_when_publishing_non_existent_article():
    article_repo, _ = _create_repositories()
    publisher = ArticlePublisher(article_repo)

    with pytest.raises(ArticleNotFound):
        publisher.execute("non-existent-id")


def test_should_raise_error_when_unpublishing_non_existent_article():
    article_repo, _ = _create_repositories()
    publisher = ArticlePublisher(article_repo)

    with pytest.raises(ArticleNotFound):
        publisher.unpublish("non-existent-id")


def test_should_record_published_event():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    # Clear creation event
    article.pull_domain_events()
    publisher = ArticlePublisher(article_repo)

    published = publisher.execute(article.id)
    events = published.pull_domain_events()

    assert len(events) == 1
    assert events[0].event_type == "ArticlePublishedEvent"


def test_should_record_unpublished_event():
    article_repo, user_repo = _create_repositories()
    article = _create_article(article_repo, user_repo)
    # Clear creation event
    article.pull_domain_events()
    publisher = ArticlePublisher(article_repo)

    publisher.execute(article.id)
    published = article_repo.find_one(article.id)
    assert published is not None
    published.pull_domain_events()  # clear publish event

    unpublished = publisher.unpublish(article.id)
    events = unpublished.pull_domain_events()

    assert len(events) == 1
    assert events[0].event_type == "ArticleUnpublishedEvent"
