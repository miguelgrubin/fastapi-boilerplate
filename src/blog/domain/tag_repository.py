from typing import List, Optional

from abc import ABC, abstractmethod

from src.blog.domain.tag import Tag


class TagRepository(ABC):
    """Abstract repository for Tag entities."""

    @abstractmethod
    def save(self, tag: Tag) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_one(self, tag_id: str) -> Optional[Tag]:
        raise NotImplementedError

    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[Tag]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> List[Tag]:
        raise NotImplementedError
