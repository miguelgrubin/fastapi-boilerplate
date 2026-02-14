from fastapi import FastAPI

from src.blog import (
    USER_CREATOR,
    USER_DELETER,
)
from src.blog.domain.article_repository import ARTICLE_REPOSITORY
from src.blog.domain.user_repository import USER_REPOSITORY
from src.blog.infrastructure.server.error_handler import blog_error_handler
from src.blog.infrastructure.server.router import blog_routes
from src.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from src.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from src.blog.types import (
    BlogRepositoriesType,
    BlogUseCasesType,
)
from src.blog.use_cases.user_creator import UserCreator
from src.blog.use_cases.user_deleter import UserDeleter
from src.shared.domain.services.password_service import PASSWORD_SERVICE
from src.shared.factory import create_password_service
from src.shared.types import SharedServicesType


def create_services() -> SharedServicesType:
    return {PASSWORD_SERVICE: create_password_service("argon2")}


def create_repositories() -> BlogRepositoriesType:
    return {
        USER_REPOSITORY: UserRepositoryMemory(),
        ARTICLE_REPOSITORY: ArticleRepositoryMemory(),
    }


def create_use_cases(
    repositories: BlogRepositoriesType, services: SharedServicesType
) -> BlogUseCasesType:
    return {
        USER_CREATOR: UserCreator(
            user_repository=repositories[USER_REPOSITORY],
            password_service=services[PASSWORD_SERVICE],
        ),
        USER_DELETER: UserDeleter(
            user_repository=repositories[USER_REPOSITORY],
        ),
    }


def create_blog_http_server(app: FastAPI):
    _, __, use_cases = create_blog_module()
    blog_error_handler(app)
    blog_routes(app, use_cases)


def create_blog_module():
    services = create_services()
    repositories = create_repositories()
    use_cases = create_use_cases(repositories, services)
    return services, repositories, use_cases
