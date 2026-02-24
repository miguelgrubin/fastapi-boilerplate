from typing import List, Optional

from src.blog.domain.article import Article
from src.blog.domain.article_repository import ArticleRepository
from src.blog.domain.errors.user_not_found import UserNotFound
from src.blog.domain.user_repository import UserRepository
from src.shared.use_cases.use_case import UseCase


class ArticleCreator(UseCase):
    def __init__(
        self,
        article_repository: ArticleRepository,
        user_repository: UserRepository,
    ) -> None:
        self.article_repository = article_repository
        self.user_repository = user_repository

    def execute(
        self,
        title: str,
        description: str,
        content: str,
        slug: str,
        author_id: str,
        category_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Article:
        author = self.user_repository.find_one(author_id)
        if not author:
            raise UserNotFound(author_id)

        article = Article.create(
            title=title,
            description=description,
            content=content,
            slug=slug,
            author_id=author_id,
            category_id=category_id,
            tags=tags,
        )
        self.article_repository.save(article)
        return article
