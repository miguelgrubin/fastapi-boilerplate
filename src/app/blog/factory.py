from fastapi import FastAPI

from app.blog import (
    ARTICLE_REPOSITORY,
    USER_CREATOR,
    USER_REPOSITORY,
)
from app.blog.infrastructure.server.user_routes import user_routes
from app.blog.infrastructure.storage.article_repository_memory import ArticleRepositoryMemory
from app.blog.infrastructure.storage.user_repository_memory import UserRepositoryMemory
from app.blog.types import (
    RepositoriesType,
    ServicesType,
    UseCasesType,
)
from app.blog.use_cases.user_creator import UserCreator
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
        )
    }


def create_server(use_cases: UseCasesType) -> FastAPI:
    blog_app = FastAPI()
    user_routes(blog_app, use_cases)
    return blog_app


def create_blog() -> FastAPI:
    services = create_services()
    repositories = create_repositories()
    use_cases = create_use_cases(repositories, services)
    server = create_server(use_cases)
    return server
