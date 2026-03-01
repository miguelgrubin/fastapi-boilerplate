from typing import Dict, List, Optional, Tuple

from sqlalchemy import delete, insert, select
from src.blog.domain.article import Article
from src.blog.domain.article_repository import ArticleRepository
from src.blog.infrastructure.storage.sql_tables import article_tags_table, articles_table
from src.shared.domain.services.sql_service import SqlService


class ArticleRepositorySql(ArticleRepository):
    def __init__(self, sql_service: SqlService) -> None:
        self._sql_service = sql_service

    def save(self, article: Article) -> None:
        with self._sql_service.session() as conn:
            existing = conn.execute(
                select(articles_table).where(articles_table.c.id == article.id)
            ).fetchone()

            if existing:
                conn.execute(
                    articles_table.update()
                    .where(articles_table.c.id == article.id)
                    .values(**self._to_row(article))
                )
            else:
                conn.execute(insert(articles_table).values(**self._to_row(article)))

            # Sync article_tags join table
            conn.execute(
                delete(article_tags_table).where(article_tags_table.c.article_id == article.id)
            )
            for tag_id in article.tags:
                conn.execute(
                    insert(article_tags_table).values(article_id=article.id, tag_id=tag_id)
                )

    def delete(self, article_id: str) -> None:
        with self._sql_service.session() as conn:
            conn.execute(
                delete(article_tags_table).where(article_tags_table.c.article_id == article_id)
            )
            conn.execute(delete(articles_table).where(articles_table.c.id == article_id))

    def find_one(self, article_id: str) -> Optional[Article]:
        with self._sql_service.session() as conn:
            row = conn.execute(
                select(articles_table).where(articles_table.c.id == article_id)
            ).fetchone()
            if row is None:
                return None
            tags = self._load_tags(conn, article_id)
            return self._to_entity(row, tags)

    def find_by_slug(self, slug: str) -> Optional[Article]:
        with self._sql_service.session() as conn:
            row = conn.execute(
                select(articles_table).where(articles_table.c.slug == slug)
            ).fetchone()
            if row is None:
                return None
            tags = self._load_tags(conn, row.id)
            return self._to_entity(row, tags)

    def find_all(
        self, find_filters: Dict, find_order: Dict, find_limits: Tuple[int, int]
    ) -> List[Article]:
        with self._sql_service.session() as conn:
            query = select(articles_table)

            offset, limit = find_limits
            query = query.offset(offset).limit(limit)

            rows = conn.execute(query).fetchall()
            articles = []
            for row in rows:
                tags = self._load_tags(conn, row.id)
                articles.append(self._to_entity(row, tags))
            return articles

    @staticmethod
    def _load_tags(conn, article_id: str) -> List[str]:
        """Load tag IDs for an article from the join table."""
        tag_rows = conn.execute(
            select(article_tags_table.c.tag_id).where(article_tags_table.c.article_id == article_id)
        ).fetchall()
        return [r.tag_id for r in tag_rows]

    @staticmethod
    def _to_row(article: Article) -> dict:
        """Map a domain Article entity to a database row dictionary."""
        return {
            "id": article.id,
            "title": article.title,
            "description": article.description,
            "content": article.content,
            "slug": article.slug,
            "author_id": article.author_id,
            "published": article.published,
            "category_id": article.category_id,
            "created_at": article.created_at,
            "updated_at": article.updated_at,
        }

    @staticmethod
    def _to_entity(row, tags: List[str]) -> Article:
        """Map a database row to a domain Article entity."""
        return Article(
            id=row.id,
            title=row.title,
            description=row.description,
            content=row.content,
            slug=row.slug,
            author_id=row.author_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
            published=row.published,
            category_id=row.category_id,
            tags=tags,
        )
