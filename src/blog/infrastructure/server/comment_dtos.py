from datetime import datetime

from pydantic import BaseModel


class CommentCreationDTO(BaseModel):
    content: str
    author_id: str


class CommentResponse(BaseModel):
    id: str
    content: str
    author_id: str
    article_id: str
    created_at: datetime
    updated_at: datetime
