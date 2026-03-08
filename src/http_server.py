from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.blog.factory import create_blog_http_server
from src.settings import settings

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)  # ty: ignore[invalid-argument-type]


@app.get("/checkhealth")
def checkhealth():
    return {"ping": "pong"}


create_blog_http_server(app)
