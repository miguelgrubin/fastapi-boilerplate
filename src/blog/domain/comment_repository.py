from typing import List, Optional, Tuple

from abc import ABC, abstractmethod

from src.blog.domain.comment import Comment


class CommentRepository(ABC):
    """Abstract repository for Comment entities."""

    @abstractmethod
    def save(self, comment: Comment) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, comment_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_one(self, comment_id: str) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def find_by_article_id(self, article_id: str) -> List[Comment]:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        article_id: Optional[str] = None,
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> List[Tuple[Comment, float]]:
        """Search comments by semantic similarity.

        Args:
            query: Search query text
            article_id: Optional filter to search within specific article
            top_k: Number of results to return
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of (Comment, similarity_score) tuples, ordered by relevance

        Raises:
            EmbeddingServiceError: If embedding generation fails
        """
        raise NotImplementedError
