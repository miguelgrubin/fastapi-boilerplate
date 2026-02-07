from typing import List, NoReturn, Optional

import copy

from app.blog.domain.article import Article
from app.blog.domain.article_repository import ArticleRepository


class ArticleRepositoryMemory(ArticleRepository):
    """docstring for ArticleRepository"""

    _articles: List[Article] = []

    def save(self, article: Article) -> NoReturn:
        self._articles.append(article)

    def delete(self, article_id: str) -> NoReturn:
        raise NotImplementedError

    def find_one(self, article_id: str) -> Optional[Article]:
        return next(filter(lambda x: x.id == article_id, self._articles), None)

    def find_all(self) -> List[Article]:
        filtered_articles = copy(self._articles)
        return filtered_articles
