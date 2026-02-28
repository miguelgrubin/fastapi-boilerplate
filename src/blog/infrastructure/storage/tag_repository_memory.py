from typing import List, Optional

from dataclasses import dataclass, field

from src.blog.domain.tag import Tag
from src.blog.domain.tag_repository import TagRepository


@dataclass
class TagRepositoryMemory(TagRepository):
    """In-memory implementation of TagRepository."""

    _tags: List[Tag] = field(default_factory=list)

    def save(self, tag: Tag) -> None:
        self._tags.append(tag)

    def find_one(self, tag_id: str) -> Optional[Tag]:
        return next(filter(lambda x: x.id == tag_id, self._tags), None)

    def find_by_slug(self, slug: str) -> Optional[Tag]:
        return next(filter(lambda x: x.slug == slug, self._tags), None)

    def find_all(self) -> List[Tag]:
        return list(self._tags)

    def clear(self) -> None:
        self._tags = []
