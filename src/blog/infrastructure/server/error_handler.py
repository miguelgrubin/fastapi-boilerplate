from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.blog.domain.errors.article_not_found import ArticleNotFound
from src.blog.domain.errors.user_not_following import UserNotFollowing
from src.blog.domain.errors.user_not_found import UserNotFound


def blog_error_handler(app: FastAPI) -> None:
    @app.exception_handler(ArticleNotFound)
    async def article_not_found_exception_handler(request, exc):
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
