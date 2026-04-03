from typing import Dict, List, Optional, Tuple

from sqlalchemy import delete, insert, select, text
from src.blog.domain.article import Article
from src.blog.domain.article_repository import ArticleRepository
from src.blog.infrastructure.storage.sql_tables import article_tags_table, articles_table
from src.shared.domain.services.embedding_service import (
    EmbeddingService,
    EmbeddingServiceError,
)
from src.shared.domain.services.sql_service import SqlService


class ArticleRepositorySql(ArticleRepository):
    def __init__(
        self,
        sql_service: SqlService,
        embedding_service: Optional[EmbeddingService] = None,
    ) -> None:
        self._sql_service = sql_service
        self._embedding_service = embedding_service

    def save(self, article: Article) -> None:
        embedding = None
        if self._embedding_service:
            try:
                combined_text = self._combine_article_text(article)
                embedding = self._embedding_service.embed_text(combined_text)
            except EmbeddingServiceError:
                pass

        with self._sql_service.session() as conn:
            existing = conn.execute(
                select(articles_table).where(articles_table.c.id == article.id)
            ).fetchone()

            row_data = self._to_row(article)
            if embedding:
                row_data["embedding"] = embedding

            if existing:
                conn.execute(
                    articles_table.update()
                    .where(articles_table.c.id == article.id)
                    .values(**row_data)
                )
            else:
                conn.execute(insert(articles_table).values(**row_data))

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
    def _combine_article_text(article: Article) -> str:
        """Combine article fields for embedding with separators.

        Weighting strategy:
        - title: high semantic importance
        - description: medium importance
        - content: high - primary search target
        - tags: medium - metadata relevance

        Args:
            article: The article to combine text from.

        Returns:
            Combined text with field separators for better semantic understanding.
        """
        parts = []

        if article.title:
            parts.append(f"Title: {article.title}")

        if article.description:
            parts.append(f"Description: {article.description}")

        if article.content:
            parts.append(f"Content: {article.content}")

        if article.tags:
            tags_str = ", ".join(article.tags)
            parts.append(f"Tags: {tags_str}")

        return "\n".join(parts)

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

    def similarity_search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> List[Tuple[Article, float]]:
        """Search articles by semantic similarity.

        Args:
            query: Search query text
            top_k: Number of results to return
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of (Article, similarity_score) tuples, ordered by relevance

        Raises:
            EmbeddingServiceError: If embedding generation fails
        """
        if not self._embedding_service:
            raise EmbeddingServiceError("Embedding service not configured")

        try:
            query_embedding = self._embedding_service.embed_text(query)

            with self._sql_service.session() as conn:
                similarity_query = (
                    select(
                        articles_table,
                        text(f"(1 - (embedding <=> '{query_embedding}'::vector)) as similarity"),
                    )
                    .where(articles_table.c.embedding.isnot(None))
                    .order_by(text("similarity DESC"))
                    .limit(top_k)
                )

                rows = conn.execute(similarity_query).fetchall()

            articles_with_scores: List[Tuple[Article, float]] = []
            for row in rows:
                score = float(row.similarity)

                if score < score_threshold:
                    continue

                tags = self._load_tags_from_row(row.id) if hasattr(row, "id") else []
                article = self._to_entity(row, tags)
                articles_with_scores.append((article, score))

            return articles_with_scores

        except EmbeddingServiceError:
            raise
        except Exception as e:
            raise EmbeddingServiceError(f"Similarity search failed: {str(e)}") from e

    def _load_tags_from_row(self, article_id: str) -> List[str]:
        """Load tags for an article from the database."""
        with self._sql_service.session() as conn:
            return self._load_tags(conn, article_id)
