from typing import List, Optional

from sqlalchemy import delete, insert, select
from src.blog.domain.comment import Comment
from src.blog.domain.comment_repository import CommentRepository
from src.blog.infrastructure.storage.sql_tables import comments_table
from src.shared.domain.services.sql_service import SqlService


class CommentRepositorySql(CommentRepository):
    def __init__(self, sql_service: SqlService) -> None:
        self._sql_service = sql_service

    def save(self, comment: Comment) -> None:
        with self._sql_service.session() as conn:
            existing = conn.execute(
                select(comments_table).where(comments_table.c.id == comment.id)
            ).fetchone()

            if existing:
                conn.execute(
                    comments_table.update()
                    .where(comments_table.c.id == comment.id)
                    .values(**self._to_row(comment))
                )
            else:
                conn.execute(insert(comments_table).values(**self._to_row(comment)))

    def delete(self, comment_id: str) -> None:
        with self._sql_service.session() as conn:
            conn.execute(delete(comments_table).where(comments_table.c.id == comment_id))

    def find_one(self, comment_id: str) -> Optional[Comment]:
        with self._sql_service.session() as conn:
            row = conn.execute(
                select(comments_table).where(comments_table.c.id == comment_id)
            ).fetchone()
            return self._to_entity(row) if row else None

    def find_by_article_id(self, article_id: str) -> List[Comment]:
        with self._sql_service.session() as conn:
            rows = conn.execute(
                select(comments_table).where(comments_table.c.article_id == article_id)
            ).fetchall()
            return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_row(comment: Comment) -> dict:
        """Map a domain Comment entity to a database row dictionary."""
        return {
            "id": comment.id,
            "content": comment.content,
            "author_id": comment.author_id,
            "article_id": comment.article_id,
            "created_at": comment.created_at,
            "updated_at": comment.updated_at,
        }

    @staticmethod
    def _to_entity(row) -> Comment:
        """Map a database row to a domain Comment entity."""
        return Comment(
            id=row.id,
            content=row.content,
            author_id=row.author_id,
            article_id=row.article_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
