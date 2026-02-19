from fastapi import FastAPI

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
from src.shared.factory import create_password_service
from src.shared.types import SharedServices


def create_services() -> SharedServices:
    return SharedServices(password_service=create_password_service("argon2"))


def create_repositories() -> BlogRepositoriesType:
    return BlogRepositoriesType(
        user_repository=UserRepositoryMemory(),
        article_repository=ArticleRepositoryMemory(),
    )


def create_use_cases(
    repositories: BlogRepositoriesType, services: SharedServices
) -> BlogUseCasesType:

    return BlogUseCasesType(
        user_creator=UserCreator(
            user_repository=repositories.user_repository,
            password_service=services.password_service,
        ),
        user_deleter=UserDeleter(
            user_repository=repositories.user_repository,
        ),
    )


def create_blog_http_server(app: FastAPI):
    _, __, use_cases = create_blog_module()
    blog_error_handler(app)
    blog_routes(app, use_cases)


def create_blog_module() -> tuple[SharedServices, BlogRepositoriesType, BlogUseCasesType]:
    services = create_services()
    repositories = create_repositories()
    use_cases = create_use_cases(repositories, services)
    return services, repositories, use_cases
