from typing import List, Optional

from abc import ABC, abstractmethod

from src.blog.domain.category import Category


class CategoryRepository(ABC):
    """Abstract repository for Category entities."""

    @abstractmethod
    def save(self, category: Category) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_one(self, category_id: str) -> Optional[Category]:
        raise NotImplementedError

    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[Category]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Category]:
        raise NotImplementedError
