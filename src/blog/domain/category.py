"""Category Domain"""

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.shared.domain.domain_model import DomainModel


@dataclass
class Category(DomainModel):
    """Category for blog articles"""

    id: str
    name: str
    slug: str
    created_at: datetime

    @classmethod
    def create(cls, name: str, slug: str) -> "Category":
        """Factory method to create a new category."""
        id = str(uuid4())
        now = datetime.now()
        category = Category(
            id=id,
            name=name,
            slug=slug,
            created_at=now,
        )
        return category
