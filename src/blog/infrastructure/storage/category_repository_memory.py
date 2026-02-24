from typing import List, Optional

from dataclasses import dataclass, field

from src.blog.domain.category import Category
from src.blog.domain.category_repository import CategoryRepository


@dataclass
class CategoryRepositoryMemory(CategoryRepository):
    """In-memory implementation of CategoryRepository."""

    _categories: List[Category] = field(default_factory=list)

    def save(self, category: Category) -> None:
        self._categories.append(category)

    def find_one(self, category_id: str) -> Optional[Category]:
        return next(filter(lambda x: x.id == category_id, self._categories), None)

    def find_by_slug(self, slug: str) -> Optional[Category]:
        return next(filter(lambda x: x.slug == slug, self._categories), None)

    def find_all(self) -> List[Category]:
        return list(self._categories)

    def clear(self) -> None:
        self._categories = []
