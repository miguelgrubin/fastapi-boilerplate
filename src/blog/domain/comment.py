"""Comment Domain"""

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.blog.domain.events.comment_created import CommentCreated
from src.blog.domain.events.comment_deleted import CommentDeleted
from src.shared.domain.domain_model import DomainModel


@dataclass
class Comment(DomainModel):
    """Comment on a blog article"""

    id: str
    content: str
    author_id: str
    article_id: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        content: str,
        author_id: str,
        article_id: str,
    ) -> "Comment":
        """Factory method to create a new comment."""
        id = str(uuid4())
        now = datetime.now()
        comment = Comment(
            id=id,
            content=content,
            author_id=author_id,
            article_id=article_id,
            created_at=now,
            updated_at=now,
        )
        comment.record(CommentCreated(id, article_id))
        return comment

    def mark_deleted(self) -> None:
        """Record a deletion event."""
        self.record(CommentDeleted(self.id, self.article_id))
