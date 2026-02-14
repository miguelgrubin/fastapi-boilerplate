from typing import List, Optional

import copy

from src.blog.domain.article import Article
from src.blog.domain.article_repository import ArticleRepository


class ArticleRepositoryMemory(ArticleRepository):
    """docstring for ArticleRepository"""

    _articles: List[Article] = []

    def save(self, article: Article) -> None:
        self._articles.append(article)

    def delete(self, article_id: str) -> None:
        if article := self.find_one(article_id):
            self._articles.remove(article)

    def find_one(self, article_id: str) -> Optional[Article]:
        return next(filter(lambda x: x.id == article_id, self._articles), None)

    def find_all(self) -> List[Article]:
        filtered_articles = copy(self._articles)
        return filtered_articles
