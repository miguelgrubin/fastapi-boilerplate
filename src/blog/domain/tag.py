"""Tag Domain"""

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.shared.domain.domain_model import DomainModel


@dataclass
class Tag(DomainModel):
    """Tag for blog articles"""

    id: str
    name: str
    slug: str
    created_at: datetime

    @classmethod
    def create(cls, name: str, slug: str) -> "Tag":
        """Factory method to create a new tag."""
        id = str(uuid4())
        now = datetime.now()
        tag = Tag(
            id=id,
            name=name,
            slug=slug,
            created_at=now,
        )
        return tag
