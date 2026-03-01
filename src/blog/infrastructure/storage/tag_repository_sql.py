from typing import List, Optional

from sqlalchemy import insert, select
from src.blog.domain.tag import Tag
from src.blog.domain.tag_repository import TagRepository
from src.blog.infrastructure.storage.sql_tables import tags_table
from src.shared.domain.services.sql_service import SqlService


class TagRepositorySql(TagRepository):
    def __init__(self, sql_service: SqlService) -> None:
        self._sql_service = sql_service

    def save(self, tag: Tag) -> None:
        with self._sql_service.session() as conn:
            existing = conn.execute(select(tags_table).where(tags_table.c.id == tag.id)).fetchone()

            if existing:
                conn.execute(
                    tags_table.update().where(tags_table.c.id == tag.id).values(**self._to_row(tag))
                )
            else:
                conn.execute(insert(tags_table).values(**self._to_row(tag)))

    def find_one(self, tag_id: str) -> Optional[Tag]:
        with self._sql_service.session() as conn:
            row = conn.execute(select(tags_table).where(tags_table.c.id == tag_id)).fetchone()
            return self._to_entity(row) if row else None

    def find_by_slug(self, slug: str) -> Optional[Tag]:
        with self._sql_service.session() as conn:
            row = conn.execute(select(tags_table).where(tags_table.c.slug == slug)).fetchone()
            return self._to_entity(row) if row else None

    def find_all(self) -> List[Tag]:
        with self._sql_service.session() as conn:
            rows = conn.execute(select(tags_table)).fetchall()
            return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_row(tag: Tag) -> dict:
        """Map a domain Tag entity to a database row dictionary."""
        return {
            "id": tag.id,
            "name": tag.name,
            "slug": tag.slug,
            "created_at": tag.created_at,
        }

    @staticmethod
    def _to_entity(row) -> Tag:
        """Map a database row to a domain Tag entity."""
        return Tag(
            id=row.id,
            name=row.name,
            slug=row.slug,
            created_at=row.created_at,
        )
