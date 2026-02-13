from fastapi import FastAPI

from app.blog import (
    ARTICLE_REPOSITORY,
    USER_CREATOR,
    USER_DELETER,
    USER_REPOSITORY,
)
from app.blog.infrastructure.server.router import blog_routes
from app.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from app.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from app.blog.types import (
    RepositoriesType,
    ServicesType,
    UseCasesType,
)
from app.blog.use_cases.user_creator import UserCreator
from app.blog.use_cases.user_deleter import UserDeleter
from app.shared import PASSWORD_SERVICE
from app.shared.services.factories import create_password_service


def create_services() -> ServicesType:
    return {PASSWORD_SERVICE: create_password_service("argon2")}


def create_repositories() -> RepositoriesType:
    return {
        USER_REPOSITORY: UserRepositoryMemory(),
        ARTICLE_REPOSITORY: ArticleRepositoryMemory(),
    }


def create_use_cases(repositories: RepositoriesType, services: ServicesType) -> UseCasesType:
    return {
        USER_CREATOR: UserCreator(
            user_repository=repositories.get(USER_REPOSITORY),
            password_service=services.get(PASSWORD_SERVICE),
        ),
        USER_DELETER: UserDeleter(
            user_repository=repositories.get(USER_REPOSITORY),
        ),
    }


def create_blog_http_server(app: FastAPI):
    _, __, use_cases = create_blog_module()
    blog_routes(app, use_cases)


def create_blog_module():
    services = create_services()
    repositories = create_repositories()
    use_cases = create_use_cases(repositories, services)
    return services, repositories, use_cases
