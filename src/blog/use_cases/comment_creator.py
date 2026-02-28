from src.blog.domain.article_repository import ArticleRepository
from src.blog.domain.comment import Comment
from src.blog.domain.comment_repository import CommentRepository
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.domain.errors.user_not_found import UserNotFound
from src.blog.domain.user_repository import UserRepository
from src.shared.use_cases.use_case import UseCase


class CommentCreator(UseCase):
    def __init__(
        self,
        comment_repository: CommentRepository,
        article_repository: ArticleRepository,
        user_repository: UserRepository,
    ) -> None:
        self.comment_repository = comment_repository
        self.article_repository = article_repository
        self.user_repository = user_repository

    def execute(self, content: str, author_id: str, article_id: str) -> Comment:
        article = self.article_repository.find_one(article_id)
        if not article:
            raise ArticleNotFound(article_id)

        author = self.user_repository.find_one(author_id)
        if not author:
            raise UserNotFound(author_id)

        comment = Comment.create(
            content=content,
            author_id=author_id,
            article_id=article_id,
        )
        self.comment_repository.save(comment)
        return comment
