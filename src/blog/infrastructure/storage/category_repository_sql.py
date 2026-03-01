from typing import List, Optional

from sqlalchemy import insert, select
from src.blog.domain.category import Category
from src.blog.domain.category_repository import CategoryRepository
from src.blog.infrastructure.storage.sql_tables import categories_table
from src.shared.domain.services.sql_service import SqlService


class CategoryRepositorySql(CategoryRepository):
    def __init__(self, sql_service: SqlService) -> None:
        self._sql_service = sql_service

    def save(self, category: Category) -> None:
        with self._sql_service.session() as conn:
            existing = conn.execute(
                select(categories_table).where(categories_table.c.id == category.id)
            ).fetchone()

            if existing:
                conn.execute(
                    categories_table.update()
                    .where(categories_table.c.id == category.id)
                    .values(**self._to_row(category))
                )
            else:
                conn.execute(insert(categories_table).values(**self._to_row(category)))

    def find_one(self, category_id: str) -> Optional[Category]:
        with self._sql_service.session() as conn:
            row = conn.execute(
                select(categories_table).where(categories_table.c.id == category_id)
            ).fetchone()
            return self._to_entity(row) if row else None

    def find_by_slug(self, slug: str) -> Optional[Category]:
        with self._sql_service.session() as conn:
            row = conn.execute(
                select(categories_table).where(categories_table.c.slug == slug)
            ).fetchone()
            return self._to_entity(row) if row else None

    def find_all(self) -> List[Category]:
        with self._sql_service.session() as conn:
            rows = conn.execute(select(categories_table)).fetchall()
            return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_row(category: Category) -> dict:
        """Map a domain Category entity to a database row dictionary."""
        return {
            "id": category.id,
            "name": category.name,
            "slug": category.slug,
            "created_at": category.created_at,
        }

    @staticmethod
    def _to_entity(row) -> Category:
        """Map a database row to a domain Category entity."""
        return Category(
            id=row.id,
            name=row.name,
            slug=row.slug,
            created_at=row.created_at,
        )
