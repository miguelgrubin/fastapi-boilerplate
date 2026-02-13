from typing import Any, Dict, Union

from app.blog.domain.article_repository import ArticleRepository
from app.blog.domain.user_repository import UserRepository
from app.blog.use_cases.user_creator import UserCreator
from app.blog.use_cases.user_deleter import UserDeleter
from app.shared.services.domain.password_service import PasswordService

ServicesType = Dict[str, PasswordService]
RepositoriesType = Dict[str, Union[UserRepository, ArticleRepository]]
UseCasesType = Dict[str, Union[UserCreator, UserDeleter, Any]]
