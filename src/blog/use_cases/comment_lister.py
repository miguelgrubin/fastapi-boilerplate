from typing import List

from src.blog.domain.article_repository import ArticleRepository
from src.blog.domain.comment import Comment
from src.blog.domain.comment_repository import CommentRepository
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.shared.use_cases.use_case import UseCase


class CommentLister(UseCase):
    def __init__(
        self,
        comment_repository: CommentRepository,
        article_repository: ArticleRepository,
    ) -> None:
        self.comment_repository = comment_repository
        self.article_repository = article_repository

    def execute(self, article_id: str) -> List[Comment]:
        article = self.article_repository.find_one(article_id)
        if not article:
            raise ArticleNotFound(article_id)

        return self.comment_repository.find_by_article_id(article_id)
