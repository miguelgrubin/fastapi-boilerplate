from datetime import datetime

from pydantic import BaseModel


class CategoryCreationDTO(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: str
    name: str
    slug: str
    created_at: datetime
