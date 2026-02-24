from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.domain.errors.category_already_exists import CategoryAlreadyExists
from src.blog.domain.errors.category_not_found import CategoryNotFound
from src.blog.domain.errors.comment_not_found import CommentNotFound
from src.blog.domain.errors.tag_already_exists import TagAlreadyExists
from src.blog.domain.errors.tag_not_found import TagNotFound
from src.blog.domain.errors.user_already_exists import UserAlreadyExists
from src.blog.domain.errors.user_not_following import UserNotFollowing
from src.blog.domain.errors.user_not_found import UserNotFound


def blog_error_handler(app: FastAPI) -> None:
    @app.exception_handler(ArticleNotFound)
    async def article_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(CommentNotFound)
    async def comment_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(CategoryNotFound)
    async def category_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(TagNotFound)
    async def tag_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserNotFound)
    async def user_not_found_exception_handler(request, exc):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserNotFollowing)
    async def user_not_following_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UserAlreadyExists)
    async def user_already_exists_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(CategoryAlreadyExists)
    async def category_already_exists_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(TagAlreadyExists)
    async def tag_already_exists_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )
