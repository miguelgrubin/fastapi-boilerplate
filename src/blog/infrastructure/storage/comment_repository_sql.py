from typing import List, Optional, Tuple

from sqlalchemy import delete, insert, select, text
from src.blog.domain.comment import Comment
from src.blog.domain.comment_repository import CommentRepository
from src.blog.infrastructure.storage.sql_tables import comments_table
from src.shared.domain.services.embedding_service import (
    EmbeddingService,
    EmbeddingServiceError,
)
from src.shared.domain.services.sql_service import SqlService


class CommentRepositorySql(CommentRepository):
    def __init__(
        self,
        sql_service: SqlService,
        embedding_service: Optional[EmbeddingService] = None,
    ) -> None:
        self._sql_service = sql_service
        self._embedding_service = embedding_service

    def save(self, comment: Comment) -> None:
        embedding = None
        if self._embedding_service:
            try:
                embedding = self._embedding_service.embed_text(comment.content)
            except EmbeddingServiceError:
                pass

        with self._sql_service.session() as conn:
            existing = conn.execute(
                select(comments_table).where(comments_table.c.id == comment.id)
            ).fetchone()

            row_data = self._to_row(comment)
            if embedding:
                row_data["embedding"] = embedding

            if existing:
                conn.execute(
                    comments_table.update()
                    .where(comments_table.c.id == comment.id)
                    .values(**row_data)
                )
            else:
                conn.execute(insert(comments_table).values(**row_data))

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

    def similarity_search(
        self,
        query: str,
        article_id: Optional[str] = None,
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> List[Tuple[Comment, float]]:
        """Search comments by semantic similarity.

        Args:
            query: Search query text
            article_id: Optional filter to search within specific article
            top_k: Number of results to return
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of (Comment, similarity_score) tuples, ordered by relevance

        Raises:
            EmbeddingServiceError: If embedding generation fails
        """
        if not self._embedding_service:
            raise EmbeddingServiceError("Embedding service not configured")

        try:
            # Embed the query
            query_embedding = self._embedding_service.embed_text(query)

            # Build the search query
            with self._sql_service.session() as conn:
                # Base query with similarity computation
                search_query = select(
                    comments_table,
                    text(f"(1 - (embedding <=> '{query_embedding}'::vector)) as similarity"),
                ).where(comments_table.c.embedding.isnot(None))

                # Add article_id filter if provided
                if article_id:
                    search_query = search_query.where(comments_table.c.article_id == article_id)

                # Order by similarity and limit
                search_query = search_query.order_by(text("similarity DESC")).limit(top_k)

                rows = conn.execute(search_query).fetchall()

            comments_with_scores: List[Tuple[Comment, float]] = []
            for row in rows:
                score = float(row.similarity)

                # Skip results below the threshold
                if score < score_threshold:
                    continue

                # Convert row to Comment entity
                comment = self._to_entity(row)
                comments_with_scores.append((comment, score))

            return comments_with_scores

        except EmbeddingServiceError:
            raise
        except Exception as e:
            raise EmbeddingServiceError(f"Similarity search failed: {str(e)}") from e
