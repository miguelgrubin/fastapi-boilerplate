from typing import Any, Dict, Union

from src.blog.domain.article_repository import ArticleRepository
from src.blog.domain.user_repository import UserRepository
from src.blog.use_cases.user_creator import UserCreator
from src.blog.use_cases.user_deleter import UserDeleter

BlogRepositoriesType = Dict[str, Union[UserRepository, ArticleRepository]]
BlogUseCasesType = Dict[str, Union[UserCreator, UserDeleter, Any]]
