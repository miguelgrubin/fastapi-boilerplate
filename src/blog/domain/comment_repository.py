from typing import List, Optional

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
