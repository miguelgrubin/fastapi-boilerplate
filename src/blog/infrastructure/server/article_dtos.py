from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel


class ArticleCreationDTO(BaseModel):
    title: str
    description: str
    content: str
    slug: str
    author_id: str
    category_id: Optional[str] = None
    tags: List[str] = []


class ArticleUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[str] = None
    tags: Optional[List[str]] = None


class ArticleResponse(BaseModel):
    id: str
    title: str
    description: str
    content: str
    slug: str
    author_id: str
    published: bool
    category_id: Optional[str] = None
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime
