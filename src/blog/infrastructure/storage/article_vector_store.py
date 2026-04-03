"""Article vector store utilities for semantic similarity search.

This module provides utilities for managing article embeddings in pgvector,
defining the schema and configuration for article semantic search.
"""

from sqlalchemy import text
from src.shared.domain.services.sql_service import SqlService


def get_article_vector_store_table_name() -> str:
    """Get the table name for article vector store.

    Returns:
        The table name used for storing article embeddings.
    """
    return "articles"


def get_article_fields_for_embedding() -> dict[str, float]:
    """Get article fields and their embedding weights.

    Returns:
        Dictionary mapping field names to their semantic importance weights:
        - title: high semantic importance
        - description: medium importance
        - content: high - primary search target
        - tags: medium - metadata relevance
    """
    return {
        "title": 1.5,  # High importance
        "description": 1.0,  # Medium importance
        "content": 1.5,  # High - primary search target
        "tags": 1.0,  # Medium - metadata relevance
    }


def ensure_pgvector_extension(sql_service: SqlService) -> None:
    """Ensure pgvector extension is installed in PostgreSQL.

    Args:
        sql_service: The SQL service providing database connection.
    """
    try:
        with sql_service.session() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    except Exception:
        pass
