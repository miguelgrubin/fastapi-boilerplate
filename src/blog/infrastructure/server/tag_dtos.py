from datetime import datetime

from pydantic import BaseModel


class TagCreationDTO(BaseModel):
    name: str


class TagResponse(BaseModel):
    id: str
    name: str
    slug: str
    created_at: datetime
