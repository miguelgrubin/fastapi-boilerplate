from fastapi import FastAPI

from src.blog.infrastructure.server.auth_routes import auth_routes
from src.blog.infrastructure.server.error_handler import blog_error_handler
from src.blog.infrastructure.server.router import blog_routes
from src.blog.infrastructure.storage.article_repository_sql import ArticleRepositorySql
from src.blog.infrastructure.storage.category_repository_sql import CategoryRepositorySql
from src.blog.infrastructure.storage.comment_repository_sql import CommentRepositorySql
from src.blog.infrastructure.storage.sql_tables import metadata
from src.blog.infrastructure.storage.tag_repository_sql import TagRepositorySql
from src.blog.infrastructure.storage.user_repository_sql import UserRepositorySql
from src.blog.types import (
    BlogRepositoriesType,
    BlogUseCasesType,
)
from src.blog.use_cases.article_creator import ArticleCreator
from src.blog.use_cases.article_deleter import ArticleDeleter
from src.blog.use_cases.article_finder import ArticleFinder
from src.blog.use_cases.article_lister import ArticleLister
from src.blog.use_cases.article_publisher import ArticlePublisher
from src.blog.use_cases.article_updater import ArticleUpdater
from src.blog.use_cases.category_creator import CategoryCreator
from src.blog.use_cases.category_lister import CategoryLister
from src.blog.use_cases.comment_creator import CommentCreator
from src.blog.use_cases.comment_deleter import CommentDeleter
from src.blog.use_cases.comment_lister import CommentLister
from src.blog.use_cases.tag_creator import TagCreator
from src.blog.use_cases.tag_lister import TagLister
from src.blog.use_cases.user_creator import UserCreator
from src.blog.use_cases.user_deleter import UserDeleter
from src.shared.domain.services.sql_service import SqlService
from src.shared.factory import (
    create_authentication_service,
    create_authorization_service,
    create_password_service,
    create_sql_service,
)
from src.shared.types import SharedServices


def create_services(database_url: str) -> SharedServices:
    from src.settings import settings

    return SharedServices(
        password_service=create_password_service("argon2"),
        sql_service=create_sql_service(database_url, metadata),
        authentication_service=create_authentication_service(
            client_id=settings.OIDC_CLIENT_ID,
            client_secret=settings.OIDC_CLIENT_SECRET,
            issuer_url=settings.OIDC_ISSUER_URL,
        ),
        authorization_service=create_authorization_service(
            model_path=settings.CASBIN_MODEL_PATH,
            policy_path=settings.CASBIN_POLICY_PATH,
        ),
    )


def create_repositories(sql_service: SqlService) -> BlogRepositoriesType:
    return BlogRepositoriesType(
        user_repository=UserRepositorySql(sql_service),
        article_repository=ArticleRepositorySql(sql_service),
        comment_repository=CommentRepositorySql(sql_service),
        category_repository=CategoryRepositorySql(sql_service),
        tag_repository=TagRepositorySql(sql_service),
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
        article_creator=ArticleCreator(
            article_repository=repositories.article_repository,
            user_repository=repositories.user_repository,
        ),
        article_finder=ArticleFinder(
            article_repository=repositories.article_repository,
        ),
        article_lister=ArticleLister(
            article_repository=repositories.article_repository,
        ),
        article_updater=ArticleUpdater(
            article_repository=repositories.article_repository,
        ),
        article_deleter=ArticleDeleter(
            article_repository=repositories.article_repository,
        ),
        article_publisher=ArticlePublisher(
            article_repository=repositories.article_repository,
        ),
        comment_creator=CommentCreator(
            comment_repository=repositories.comment_repository,
            article_repository=repositories.article_repository,
            user_repository=repositories.user_repository,
        ),
        comment_lister=CommentLister(
            comment_repository=repositories.comment_repository,
            article_repository=repositories.article_repository,
        ),
        comment_deleter=CommentDeleter(
            comment_repository=repositories.comment_repository,
        ),
        category_creator=CategoryCreator(
            category_repository=repositories.category_repository,
        ),
        category_lister=CategoryLister(
            category_repository=repositories.category_repository,
        ),
        tag_creator=TagCreator(
            tag_repository=repositories.tag_repository,
        ),
        tag_lister=TagLister(
            tag_repository=repositories.tag_repository,
        ),
    )


def create_blog_http_server(app: FastAPI) -> None:
    services, _, use_cases = create_blog_module()
    blog_error_handler(app)
    auth_routes(app, services.authentication_service)
    blog_routes(app, use_cases, services.authentication_service, services.authorization_service)


def create_blog_module() -> tuple[SharedServices, BlogRepositoriesType, BlogUseCasesType]:
    from src.settings import settings

    database_url = str(settings.DATABASE_URL)
    services = create_services(database_url)
    repositories = create_repositories(services.sql_service)
    use_cases = create_use_cases(repositories, services)
    return services, repositories, use_cases
