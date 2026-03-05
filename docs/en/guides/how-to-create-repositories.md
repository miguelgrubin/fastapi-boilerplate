# How to Create SQL Repositories

This guide walks through adding a new SQL-backed repository to the project. It uses the
`Article` entity as a concrete example, since `UserRepositorySql` already exists as a reference
implementation.

The pattern follows hexagonal architecture: the domain defines an abstract repository port (ABC),
and we provide a concrete adapter in the infrastructure layer using SQLAlchemy Core.
```python
from abc import ABC, abstractmethod
```

## Prerequisites

Before starting, make sure:

- `SqlService` is wired in `src/shared/factory.py` and available via `SharedServices`
- Alembic is configured (`alembic/` directory, `alembic.ini`)
- You have read the existing reference implementation at
  `src/blog/infrastructure/storage/user_repository_sql.py`

## Step 1: Define the Table

All table definitions live in a single file: `src/blog/infrastructure/storage/sql_tables.py`.
This module exports a shared `metadata` object that Alembic uses for auto-generating migrations.

Add your new table below the existing ones:

```python
# src/blog/infrastructure/storage/sql_tables.py

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    JSON,
    MetaData,
    String,
    Table,
    Text,
)

metadata = MetaData()

# ... existing users_table ...

articles_table = Table(
    "articles",
    metadata,
    Column("id", String, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=False),
    Column("content", Text, nullable=False),
    Column("slug", String, unique=True, nullable=False),
    Column("author_id", String, nullable=False),
    Column("published", Boolean, nullable=False, server_default="0"),
    Column("category_id", String, nullable=True),
    Column("tags", JSON, nullable=False, server_default="[]"),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
)
```

### Column type mapping

| Python / Domain type | SQLAlchemy column type | Notes |
|----------------------|------------------------|-------|
| `str`                | `String`               | General-purpose text |
| `str` (long text)    | `Text`                 | Use for content/body fields |
| `bool`               | `Boolean`              | SQLite stores as 0/1 |
| `datetime`           | `DateTime`             | Must be `datetime` objects, not strings |
| `Optional[str]`      | `String, nullable=True`| `None` maps to SQL `NULL` |
| `List[str]`          | `JSON`                 | Serialized as JSON; see gotchas below |

## Step 2: Create the Repository Class

Create a new file at `src/blog/infrastructure/storage/article_repository_sql.py`.

The repository receives `SqlService` via constructor injection and uses it for all database
access. Every operation runs inside a `with self._sql_service.session() as conn:` block, which
auto-commits on success and auto-rolls-back on exception.

```python
# src/blog/infrastructure/storage/article_repository_sql.py

from typing import Dict, List, Optional, Tuple

import json

from sqlalchemy import delete, insert, select

from src.blog.domain.article import Article
from src.blog.domain.article_repository import ArticleRepository
from src.blog.infrastructure.storage.sql_tables import articles_table
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

    def delete(self, article_id: str) -> None:
        with self._sql_service.session() as conn:
            conn.execute(delete(articles_table).where(articles_table.c.id == article_id))

    def find_one(self, article_id: str) -> Optional[Article]:
        with self._sql_service.session() as conn:
            row = conn.execute(
                select(articles_table).where(articles_table.c.id == article_id)
            ).fetchone()
            return self._to_entity(row) if row else None

    def find_by_slug(self, slug: str) -> Optional[Article]:
        with self._sql_service.session() as conn:
            row = conn.execute(
                select(articles_table).where(articles_table.c.slug == slug)
            ).fetchone()
            return self._to_entity(row) if row else None

    def find_all(
        self, find_filters: Dict, find_order: Dict, find_limits: Tuple[int, int]
    ) -> List[Article]:
        with self._sql_service.session() as conn:
            query = select(articles_table)

            offset, limit = find_limits
            query = query.offset(offset).limit(limit)

            rows = conn.execute(query).fetchall()
            return [self._to_entity(row) for row in rows]

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
            "tags": json.dumps(article.tags),
            "created_at": article.created_at,
            "updated_at": article.updated_at,
        }

    @staticmethod
    def _to_entity(row) -> Article:  # type: ignore[no-untyped-def]
        """Map a database row to a domain Article entity."""
        tags = row.tags
        if isinstance(tags, str):
            tags = json.loads(tags)

        return Article(
            id=row.id,
            title=row.title,
            description=row.description,
            content=row.content,
            slug=row.slug,
            author_id=row.author_id,
            published=bool(row.published),
            category_id=row.category_id,
            tags=tags or [],
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
```

### Key patterns in the mapper methods

**`_to_row()` (entity -> database)**
- JSON list fields (`tags`) must be serialized with `json.dumps()` because SQLite stores JSON
  as plain text strings.
- `bool` fields are stored natively -- SQLAlchemy handles the Python `bool` to SQL integer
  mapping.
- `datetime` fields must remain as `datetime` objects. Do not convert them to strings.

**`_to_entity()` (database -> entity)**
- JSON fields need defensive deserialization: check `isinstance(value, str)` before calling
  `json.loads()`. PostgreSQL returns native Python lists from JSON columns, but SQLite returns
  strings.
- `bool` fields: wrap with `bool()` to normalize SQLite's 0/1 integers back to Python booleans.
- Nullable fields (`category_id`) map directly -- `NULL` becomes `None`.

## Step 3: Wire It in the Factory

In `src/blog/factory.py`, replace the in-memory implementation with the SQL one:

```python
# src/blog/factory.py

from src.blog.infrastructure.storage.article_repository_sql import ArticleRepositorySql

def create_repositories(sql_service: SqlService) -> BlogRepositoriesType:
    return BlogRepositoriesType(
        user_repository=UserRepositorySql(sql_service),
        article_repository=ArticleRepositorySql(sql_service),  # was ArticleRepositoryMemory()
        comment_repository=CommentRepositoryMemory(),
        category_repository=CategoryRepositoryMemory(),
        tag_repository=TagRepositoryMemory(),
    )
```

The hexagonal architecture means no other code needs to change -- use cases depend on the
`ArticleRepository` ABC, not the concrete class.

## Step 4: Generate and Run the Migration

```bash
# Generate a migration from the table diff
make migrate-create m="add articles table"

# Review the generated file in alembic/versions/
# Then apply it
make migrate
```

Always review the auto-generated migration before running it. Alembic compares the `metadata`
object in `sql_tables.py` against the current database schema and generates the diff.

## Step 5: Write Tests

Tests use an in-memory SQLite database so no external database is needed.

Create `tests/blog/infrastructure/storage/test_article_repository_sql.py`:

```python
import pytest

from src.blog.domain.article import Article
from src.blog.infrastructure.storage.sql_tables import metadata
from src.blog.infrastructure.storage.article_repository_sql import ArticleRepositorySql
from src.shared.infrastructure.services.sql_service_sqlalchemy import SqlServiceSqlAlchemy


@pytest.fixture
def sql_service():
    """Create a SqlService backed by an in-memory SQLite database."""
    service = SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)
    service.connect()
    metadata.create_all(service._engine)
    yield service
    service.disconnect()


@pytest.fixture
def repository(sql_service):
    return ArticleRepositorySql(sql_service)


def _create_article(title: str = "My Article") -> Article:
    return Article.create(
        title=title,
        description="A test article",
        content="Some content here",
        author_id="author-1",
        tags=["python", "testing"],
    )


def test_should_save_and_find_article(repository):
    article = _create_article()
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert found.id == article.id
    assert found.title == article.title
    assert found.tags == ["python", "testing"]


def test_should_find_by_slug(repository):
    article = _create_article(title="Hello World")
    repository.save(article)

    found = repository.find_by_slug(article.slug)

    assert found is not None
    assert found.title == "Hello World"


def test_should_return_none_when_not_found(repository):
    assert repository.find_one("nonexistent-id") is None
    assert repository.find_by_slug("nonexistent-slug") is None


def test_should_delete_article(repository):
    article = _create_article()
    repository.save(article)

    repository.delete(article.id)

    assert repository.find_one(article.id) is None


def test_should_update_existing_article(repository):
    article = _create_article()
    repository.save(article)

    article.update({"title": "Updated Title", "tags": ["updated"]})
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert found.title == "Updated Title"
    assert found.tags == ["updated"]


def test_should_persist_published_state(repository):
    article = _create_article()
    repository.save(article)

    article.publish()
    repository.save(article)

    found = repository.find_one(article.id)

    assert found is not None
    assert found.published is True
```

Run the tests:

```bash
uv run pytest tests/blog/infrastructure/storage/test_article_repository_sql.py -v
```

### Test fixture pattern

The fixture creates a fresh in-memory SQLite database for each test:

1. `SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)` -- creates the engine
2. `service.connect()` -- connects to the database
3. `metadata.create_all(service._engine)` -- creates all tables defined in `sql_tables.py`
4. The test runs against a clean database
5. `service.disconnect()` -- tears down the connection (the in-memory DB is discarded)

## Tips and Gotchas

### JSON columns across databases

SQLite stores JSON columns as plain text strings, while PostgreSQL uses native JSON. The
`_to_entity()` mapper handles this with a type check:

```python
tags = row.tags
if isinstance(tags, str):
    tags = json.loads(tags)
```

Always include this guard so your code works on both SQLite (tests) and PostgreSQL (production).

### DateTime columns

SQLAlchemy `DateTime` columns expect Python `datetime` objects. Never pass date strings --
SQLite will silently store them as text, and queries will behave unexpectedly.

### Upsert pattern

The `save()` method uses a SELECT-then-INSERT-or-UPDATE pattern. This works reliably for
single-writer scenarios. If you need true database-level upserts for concurrent writes,
consider using dialect-specific `INSERT ... ON CONFLICT` via
`sqlalchemy.dialects.postgresql.insert` or `sqlalchemy.dialects.sqlite.insert`.

### Adding filters to `find_all()`

The `find_filters` dict is passed from the use case layer. Extend the query with WHERE
clauses based on the filter keys:

```python
def find_all(
    self, find_filters: Dict, find_order: Dict, find_limits: Tuple[int, int]
) -> List[Article]:
    with self._sql_service.session() as conn:
        query = select(articles_table)

        if author_id := find_filters.get("author_id"):
            query = query.where(articles_table.c.author_id == author_id)
        if find_filters.get("published_only"):
            query = query.where(articles_table.c.published == True)

        offset, limit = find_limits
        query = query.offset(offset).limit(limit)

        rows = conn.execute(query).fetchall()
        return [self._to_entity(row) for row in rows]
```

## Reference

- Existing implementation: `src/blog/infrastructure/storage/user_repository_sql.py`
- Table definitions: `src/blog/infrastructure/storage/sql_tables.py`
- SqlService port: `src/shared/domain/services/sql_service.py`
- SqlService implementation: `src/shared/infrastructure/services/sql_service_sqlalchemy.py`
- Test example: `tests/blog/infrastructure/storage/test_user_repository_sql.py`
