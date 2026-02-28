from src.blog.domain.article import Article
from src.blog.domain.article_repository import ArticleRepository
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.shared.use_cases.use_case import UseCase


class ArticlePublisher(UseCase):
    def __init__(self, article_repository: ArticleRepository) -> None:
        self.article_repository = article_repository

    def execute(self, article_id: str) -> Article:
        article = self.article_repository.find_one(article_id)
        if not article:
            raise ArticleNotFound(article_id)
        article.publish()
        self.article_repository.save(article)
        return article

    def unpublish(self, article_id: str) -> Article:
        article = self.article_repository.find_one(article_id)
        if not article:
            raise ArticleNotFound(article_id)
        article.unpublish()
        self.article_repository.save(article)
        return article
