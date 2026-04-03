from typing import Dict, List, Optional, Tuple

from abc import ABC, abstractmethod

from src.blog.domain.article import Article


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
    def find_all(
        self, find_filters: Dict, find_order: Dict, find_limits: Tuple[int, int]
    ) -> List[Article]:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> List[Tuple[Article, float]]:
        """Search articles by semantic similarity.

        Args:
            query: Search query text
            top_k: Number of results to return
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of (Article, similarity_score) tuples, ordered by relevance

        Raises:
            EmbeddingServiceError: If embedding generation fails
        """
        raise NotImplementedError
