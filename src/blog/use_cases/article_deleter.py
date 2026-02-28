from src.blog.domain.article_repository import ArticleRepository
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.shared.use_cases.use_case import UseCase


class ArticleDeleter(UseCase):
    def __init__(self, article_repository: ArticleRepository) -> None:
        self.article_repository = article_repository

    def execute(self, article_id: str) -> None:
        article = self.article_repository.find_one(article_id)
        if not article:
            raise ArticleNotFound(article_id)
        self.article_repository.delete(article_id)
