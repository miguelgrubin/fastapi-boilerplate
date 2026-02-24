from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.article_lister import ArticleLister
from src.blog.use_cases.user_creator import UserCreator
from src.shared.infrastructure.services.password_service_fake import PasswordServiceFake


def _create_repositories():
    article_repo = ArticleRepositoryMemory()
    article_repo.clear()
    user_repo = UserRepositoryMemory()
    user_repo.clear()
    return article_repo, user_repo


def _create_user(user_repo):
    password_service = PasswordServiceFake()
    return UserCreator(user_repo, password_service).execute(
        "author", "S3CUR€ PA$$", "author@example.com"
    )


def test_should_return_empty_list_when_no_articles():
    article_repo, _ = _create_repositories()
    lister = ArticleLister(article_repo)

    articles = lister.execute()

    assert articles == []


def test_should_return_all_articles():
    article_repo, user_repo = _create_repositories()
    user = _create_user(user_repo)
    creator = ArticleCreator(article_repo, user_repo)

    creator.execute("First", "Summary 1", "Content 1", "first", user.id)
    creator.execute("Second", "Summary 2", "Content 2", "second", user.id)
    creator.execute("Third", "Summary 3", "Content 3", "third", user.id)

    lister = ArticleLister(article_repo)
    articles = lister.execute()

    assert len(articles) == 3
