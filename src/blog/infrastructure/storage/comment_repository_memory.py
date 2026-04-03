from typing import List, Optional, Tuple

from dataclasses import dataclass, field

from src.blog.domain.comment import Comment
from src.blog.domain.comment_repository import CommentRepository
from src.shared.domain.services.embedding_service import EmbeddingServiceError


@dataclass
class CommentRepositoryMemory(CommentRepository):
    """In-memory implementation of CommentRepository."""

    _comments: List[Comment] = field(default_factory=list)

    def save(self, comment: Comment) -> None:
        self._comments.append(comment)

    def delete(self, comment_id: str) -> None:
        if comment := self.find_one(comment_id):
            self._comments.remove(comment)

    def find_one(self, comment_id: str) -> Optional[Comment]:
        return next(filter(lambda x: x.id == comment_id, self._comments), None)

    def find_by_article_id(self, article_id: str) -> List[Comment]:
        return list(filter(lambda x: x.article_id == article_id, self._comments))

    def similarity_search(
        self,
        query: str,
        article_id: Optional[str] = None,
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> List[Tuple[Comment, float]]:
        raise EmbeddingServiceError("Semantic search not supported in memory repository")

    def clear(self) -> None:
        self._comments = []
