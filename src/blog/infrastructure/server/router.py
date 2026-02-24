from typing import List, cast

from fastapi import FastAPI, Response
from src.blog.domain.article import ArticleUpdateParams
from src.blog.infrastructure.mappers.article_mapper import ArticleMapper
from src.blog.infrastructure.mappers.category_mapper import CategoryMapper
from src.blog.infrastructure.mappers.comment_mapper import CommentMapper
from src.blog.infrastructure.mappers.tag_mapper import TagMapper
from src.blog.infrastructure.mappers.user_mapper import UserMapper
from src.blog.infrastructure.server.article_dtos import (
    ArticleCreationDTO,
    ArticleResponse,
    ArticleUpdateDTO,
)
from src.blog.infrastructure.server.category_dtos import (
    CategoryCreationDTO,
    CategoryResponse,
)
from src.blog.infrastructure.server.comment_dtos import CommentCreationDTO, CommentResponse
from src.blog.infrastructure.server.tag_dtos import TagCreationDTO, TagResponse
from src.blog.infrastructure.server.user_dtos import UserCreationDTO, UserResponse
from src.blog.types import BlogUseCasesType
from src.blog.use_cases.user_creator import UserCreator
from src.blog.use_cases.user_deleter import UserDeleter


def blog_routes(app: FastAPI, use_cases: BlogUseCasesType) -> None:
    # ---- User routes ----

    @app.post("/app/v1/blog/users", response_model=UserResponse)
    def create_user(payload: UserCreationDTO) -> UserResponse:
        use_case: UserCreator = use_cases.user_creator
        user = use_case.execute(payload.username, payload.password, payload.email)
        return UserMapper.to_dto(user)

    @app.delete("/admin/v1/blog/users/{user_id}", status_code=204)
    def delete_user(user_id: str) -> Response:
        use_case: UserDeleter = use_cases.user_deleter
        use_case.execute(user_id)
        return Response(status_code=204)

    # ---- Article routes ----

    @app.post("/app/v1/blog/articles", response_model=ArticleResponse, status_code=201)
    def create_article(payload: ArticleCreationDTO) -> ArticleResponse:
        article = use_cases.article_creator.execute(
            title=payload.title,
            description=payload.description,
            content=payload.content,
            slug=payload.slug,
            author_id=payload.author_id,
            category_id=payload.category_id,
            tags=payload.tags,
        )
        return ArticleMapper.to_dto(article)

    @app.get("/app/v1/blog/articles", response_model=List[ArticleResponse])
    def list_articles() -> List[ArticleResponse]:
        articles = use_cases.article_lister.execute()
        return [ArticleMapper.to_dto(article) for article in articles]

    @app.get("/app/v1/blog/articles/{article_id}", response_model=ArticleResponse)
    def get_article(article_id: str) -> ArticleResponse:
        article = use_cases.article_finder.execute(article_id)
        return ArticleMapper.to_dto(article)

    @app.get("/app/v1/blog/articles/slug/{slug}", response_model=ArticleResponse)
    def get_article_by_slug(slug: str) -> ArticleResponse:
        article = use_cases.article_finder.execute_by_slug(slug)
        return ArticleMapper.to_dto(article)

    @app.put("/app/v1/blog/articles/{article_id}", response_model=ArticleResponse)
    def update_article(article_id: str, payload: ArticleUpdateDTO) -> ArticleResponse:
        update_params = cast(ArticleUpdateParams, payload.model_dump(exclude_none=True))
        article = use_cases.article_updater.execute(article_id, update_params)
        return ArticleMapper.to_dto(article)

    @app.delete("/app/v1/blog/articles/{article_id}", status_code=204)
    def delete_article(article_id: str) -> Response:
        use_cases.article_deleter.execute(article_id)
        return Response(status_code=204)

    @app.post("/app/v1/blog/articles/{article_id}/publish", response_model=ArticleResponse)
    def publish_article(article_id: str) -> ArticleResponse:
        article = use_cases.article_publisher.execute(article_id)
        return ArticleMapper.to_dto(article)

    @app.post("/app/v1/blog/articles/{article_id}/unpublish", response_model=ArticleResponse)
    def unpublish_article(article_id: str) -> ArticleResponse:
        article = use_cases.article_publisher.unpublish(article_id)
        return ArticleMapper.to_dto(article)

    # ---- Comment routes ----

    @app.post(
        "/app/v1/blog/articles/{article_id}/comments",
        response_model=CommentResponse,
        status_code=201,
    )
    def create_comment(article_id: str, payload: CommentCreationDTO) -> CommentResponse:
        comment = use_cases.comment_creator.execute(
            content=payload.content,
            author_id=payload.author_id,
            article_id=article_id,
        )
        return CommentMapper.to_dto(comment)

    @app.get(
        "/app/v1/blog/articles/{article_id}/comments",
        response_model=List[CommentResponse],
    )
    def list_comments(article_id: str) -> List[CommentResponse]:
        comments = use_cases.comment_lister.execute(article_id)
        return [CommentMapper.to_dto(comment) for comment in comments]

    @app.delete("/app/v1/blog/comments/{comment_id}", status_code=204)
    def delete_comment(comment_id: str) -> Response:
        use_cases.comment_deleter.execute(comment_id)
        return Response(status_code=204)

    # ---- Category routes ----

    @app.post(
        "/app/v1/blog/categories",
        response_model=CategoryResponse,
        status_code=201,
    )
    def create_category(payload: CategoryCreationDTO) -> CategoryResponse:
        category = use_cases.category_creator.execute(
            name=payload.name,
            slug=payload.slug,
        )
        return CategoryMapper.to_dto(category)

    @app.get("/app/v1/blog/categories", response_model=List[CategoryResponse])
    def list_categories() -> List[CategoryResponse]:
        categories = use_cases.category_lister.execute()
        return [CategoryMapper.to_dto(category) for category in categories]

    # ---- Tag routes ----

    @app.post(
        "/app/v1/blog/tags",
        response_model=TagResponse,
        status_code=201,
    )
    def create_tag(payload: TagCreationDTO) -> TagResponse:
        tag = use_cases.tag_creator.execute(
            name=payload.name,
            slug=payload.slug,
        )
        return TagMapper.to_dto(tag)

    @app.get("/app/v1/blog/tags", response_model=List[TagResponse])
    def list_tags() -> List[TagResponse]:
        tags = use_cases.tag_lister.execute()
        return [TagMapper.to_dto(tag) for tag in tags]
