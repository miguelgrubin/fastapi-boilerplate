from src.blog.domain.comment_repository import CommentRepository
from src.blog.domain.errors.comment_not_found import CommentNotFound
from src.shared.use_cases.use_case import UseCase


class CommentDeleter(UseCase):
    def __init__(self, comment_repository: CommentRepository) -> None:
        self.comment_repository = comment_repository

    def execute(self, comment_id: str) -> None:
        comment = self.comment_repository.find_one(comment_id)
        if not comment:
            raise CommentNotFound(comment_id)
        comment.mark_deleted()
        self.comment_repository.delete(comment_id)
