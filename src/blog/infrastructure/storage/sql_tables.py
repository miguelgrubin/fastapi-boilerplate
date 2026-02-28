"""SQLAlchemy Core table definitions.

This module is the single source of truth for all database table schemas.
Alembic auto-generates migrations from the `metadata` object defined here.

To add a new table:
    1. Define a new Table(...) bound to `metadata`
    2. Run: make migrate-create m="description of change"
    3. Review the generated migration in alembic/versions/
    4. Run: make migrate
"""

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
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
