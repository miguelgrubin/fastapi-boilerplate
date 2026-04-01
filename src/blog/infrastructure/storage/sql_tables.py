"""SQLAlchemy Core table definitions.

This module is the single source of truth for all database table schemas.
Alembic auto-generates migrations from the `metadata` object defined here.

To add a new table:
    1. Define a new Table(...) bound to `metadata`
    2. Run: make migrate-create m="description of change"
    3. Review the generated migration in alembic/versions/
    4. Run: make migrate
"""

from pgvector.sqlalchemy import Vector  # type: ignore[import-not-found]  # noqa: F811
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    MetaData,
    String,
    Table,
)

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", String, primary_key=True),
    Column("email", String, unique=True, nullable=False),
    Column("username", String, unique=True, nullable=False),
    Column("password_hash", String, nullable=False),
    Column("bio", String, nullable=True),
    Column("image", String, nullable=True),
    Column("following", JSON, nullable=False, server_default="[]"),
    Column("followers", JSON, nullable=False, server_default="[]"),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)

categories_table = Table(
    "categories",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String, unique=True, nullable=False),
    Column("slug", String, unique=True, nullable=False),
    Column("created_at", DateTime, nullable=False),
)

tags_table = Table(
    "tags",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String, unique=True, nullable=False),
    Column("slug", String, unique=True, nullable=False),
    Column("created_at", DateTime, nullable=False),
)

articles_table = Table(
    "articles",
    metadata,
    Column("id", String, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("content", String, nullable=False),
    Column("slug", String, unique=True, nullable=False),
    Column("author_id", String, ForeignKey("users.id"), nullable=False),
    Column("published", Boolean, nullable=False, server_default="false"),
    Column("category_id", String, ForeignKey("categories.id"), nullable=True),
    Column("embedding", Vector(1536), nullable=True),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)

article_tags_table = Table(
    "article_tags",
    metadata,
    Column("article_id", String, ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", String, ForeignKey("tags.id"), primary_key=True),
)

comments_table = Table(
    "comments",
    metadata,
    Column("id", String, primary_key=True),
    Column("content", String, nullable=False),
    Column("author_id", String, ForeignKey("users.id"), nullable=False),
    Column("article_id", String, ForeignKey("articles.id"), nullable=False),
    Column("embedding", Vector(1536), nullable=True),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)
