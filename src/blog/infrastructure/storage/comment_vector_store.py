"""Comment vector store utilities for semantic similarity search.

This module provides utilities for managing comment embeddings in pgvector,
defining the schema and configuration for comment semantic search.
"""

from sqlalchemy import text
from src.shared.domain.services.sql_service import SqlService


def get_comment_vector_store_table_name() -> str:
    """Get the table name for comment vector store.

    Returns:
        The table name used for storing comment embeddings.
    """
    return "comments"


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
