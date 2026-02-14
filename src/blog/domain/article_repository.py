from typing import List, Optional

from abc import ABC, abstractmethod

from src.blog.domain.article import Article

ARTICLE_REPOSITORY = "ArticleRepository"


class ArticleRepository(ABC):
    """docstring for ArticleRepository"""

    @abstractmethod
    def save(self, article: Article) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, article_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_one(self, article_id: str) -> Optional[Article]:
        raise NotImplementedError

    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[Article]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, find_filters, find_order, find_limits) -> List[Article]:
        raise NotImplementedError
