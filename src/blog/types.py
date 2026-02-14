from dataclasses import dataclass

from src.blog.domain.article_repository import ArticleRepository
from src.blog.domain.user_repository import UserRepository
from src.blog.use_cases.user_creator import UserCreator
from src.blog.use_cases.user_deleter import UserDeleter


@dataclass
class BlogRepositoriesType:
    user_repository: UserRepository
    article_repository: ArticleRepository


@dataclass
class BlogUseCasesType:
    user_creator: UserCreator
    user_deleter: UserDeleter
