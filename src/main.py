from fastapi import FastAPI

from app.blog.factory import create_blog_http_server

app = FastAPI()


@app.get("/checkhealth")
def checkhealth():
    return {"ping": "pong"}


blog_app = create_blog_http_server(app)
