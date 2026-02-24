from src.blog.domain.comment import Comment
from src.blog.infrastructure.server.comment_dtos import CommentResponse


class CommentMapper:
    @staticmethod
    def to_dto(comment: Comment) -> CommentResponse:
        return CommentResponse(
            id=comment.id,
            content=comment.content,
            author_id=comment.author_id,
            article_id=comment.article_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
