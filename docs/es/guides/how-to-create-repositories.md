# Como Crear Repositorios SQL

Esta guia explica paso a paso como agregar un nuevo repositorio respaldado por SQL al proyecto.
Usa la entidad `Article` como ejemplo concreto, ya que `UserRepositorySql` ya existe como
implementacion de referencia.

El patron sigue la arquitectura hexagonal: el dominio define un puerto de repositorio abstracto (ABC),
y proporcionamos un adaptador concreto en la capa de infraestructura usando SQLAlchemy Core.

## Prerrequisitos

Antes de empezar, asegurate de que:

- `SqlService` esta conectado en `src/shared/factory.py` y disponible via `SharedServices`
- Alembic esta configurado (directorio `alembic/`, `alembic.ini`)
- Has leido la implementacion de referencia existente en
  `src/blog/infrastructure/storage/user_repository_sql.py`

## Paso 1: Definir la Tabla

Todas las definiciones de tablas viven en un unico archivo: `src/blog/infrastructure/storage/sql_tables.py`.
Este modulo exporta un objeto `metadata` compartido que Alembic usa para auto-generar migraciones.

Agrega tu nueva tabla debajo de las existentes:

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

# ... users_table existente ...

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

### Mapeo de tipos de columna

| Tipo Python / Dominio  | Tipo de columna SQLAlchemy | Notas |
|-------------------------|----------------------------|-------|
| `str`                   | `String`                   | Texto de proposito general |
| `str` (texto largo)     | `Text`                     | Usar para campos de contenido/cuerpo |
| `bool`                  | `Boolean`                  | SQLite almacena como 0/1 |
| `datetime`              | `DateTime`                 | Deben ser objetos `datetime`, no strings |
| `Optional[str]`         | `String, nullable=True`    | `None` se mapea a SQL `NULL` |
| `List[str]`             | `JSON`                     | Serializado como JSON; ver notas abajo |

## Paso 2: Crear la Clase del Repositorio

Crea un nuevo archivo en `src/blog/infrastructure/storage/article_repository_sql.py`.

El repositorio recibe `SqlService` via inyeccion en el constructor y lo usa para todo el acceso
a la base de datos. Cada operacion se ejecuta dentro de un bloque `with self._sql_service.session() as conn:`,
que hace auto-commit en caso de exito y auto-rollback en caso de excepcion.

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
        """Mapea una entidad Article del dominio a un diccionario de fila de base de datos."""
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
        """Mapea una fila de base de datos a una entidad Article del dominio."""
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

### Patrones clave en los metodos mapper

**`_to_row()` (entidad -> base de datos)**
- Los campos de lista JSON (`tags`) deben serializarse con `json.dumps()` porque SQLite almacena JSON
  como cadenas de texto plano.
- Los campos `bool` se almacenan nativamente -- SQLAlchemy maneja el mapeo de `bool` de Python a entero
  SQL.
- Los campos `datetime` deben permanecer como objetos `datetime`. No los conviertas a strings.

**`_to_entity()` (base de datos -> entidad)**
- Los campos JSON necesitan deserializacion defensiva: verifica `isinstance(value, str)` antes de llamar
  a `json.loads()`. PostgreSQL devuelve listas nativas de Python desde columnas JSON, pero SQLite devuelve
  strings.
- Campos `bool`: envuelve con `bool()` para normalizar los enteros 0/1 de SQLite de vuelta a booleanos de Python.
- Campos nullables (`category_id`) se mapean directamente -- `NULL` se convierte en `None`.

## Paso 3: Conectarlo en la Factory

En `src/blog/factory.py`, reemplaza la implementacion en memoria con la SQL:

```python
# src/blog/factory.py

from src.blog.infrastructure.storage.article_repository_sql import ArticleRepositorySql

def create_repositories(sql_service: SqlService) -> BlogRepositoriesType:
    return BlogRepositoriesType(
        user_repository=UserRepositorySql(sql_service),
        article_repository=ArticleRepositorySql(sql_service),  # antes era ArticleRepositoryMemory()
        comment_repository=CommentRepositoryMemory(),
        category_repository=CategoryRepositoryMemory(),
        tag_repository=TagRepositoryMemory(),
    )
```

La arquitectura hexagonal significa que ningun otro codigo necesita cambiar -- los casos de uso dependen del
ABC `ArticleRepository`, no de la clase concreta.

## Paso 4: Generar y Ejecutar la Migracion

```bash
# Generar una migracion a partir del diff de tablas
make migrate-create m="add articles table"

# Revisar el archivo generado en alembic/versions/
# Luego aplicarla
make migrate
```

Siempre revisa la migracion auto-generada antes de ejecutarla. Alembic compara el objeto `metadata`
en `sql_tables.py` contra el esquema actual de la base de datos y genera el diff.

## Paso 5: Escribir Tests

Los tests usan una base de datos SQLite en memoria, por lo que no se necesita una base de datos externa.

Crea `tests/blog/infrastructure/storage/test_article_repository_sql.py`:

```python
import pytest

from src.blog.domain.article import Article
from src.blog.infrastructure.storage.sql_tables import metadata
from src.blog.infrastructure.storage.article_repository_sql import ArticleRepositorySql
from src.shared.infrastructure.services.sql_service_sqlalchemy import SqlServiceSqlAlchemy


@pytest.fixture
def sql_service():
    """Crea un SqlService respaldado por una base de datos SQLite en memoria."""
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

Ejecuta los tests:

```bash
uv run pytest tests/blog/infrastructure/storage/test_article_repository_sql.py -v
```

### Patron de fixtures de test

El fixture crea una base de datos SQLite en memoria fresca para cada test:

1. `SqlServiceSqlAlchemy("sqlite:///:memory:", metadata)` -- crea el motor
2. `service.connect()` -- se conecta a la base de datos
3. `metadata.create_all(service._engine)` -- crea todas las tablas definidas en `sql_tables.py`
4. El test se ejecuta contra una base de datos limpia
5. `service.disconnect()` -- destruye la conexion (la BD en memoria se descarta)

## Consejos y Notas Importantes

### Columnas JSON entre bases de datos

SQLite almacena columnas JSON como cadenas de texto plano, mientras que PostgreSQL usa JSON nativo. El
mapper `_to_entity()` maneja esto con una verificacion de tipo:

```python
tags = row.tags
if isinstance(tags, str):
    tags = json.loads(tags)
```

Incluye siempre esta verificacion para que tu codigo funcione tanto en SQLite (tests) como en PostgreSQL (produccion).

### Columnas DateTime

Las columnas `DateTime` de SQLAlchemy esperan objetos `datetime` de Python. Nunca pases cadenas de fecha --
SQLite las almacenara silenciosamente como texto, y las consultas se comportaran de forma inesperada.

### Patron Upsert

El metodo `save()` usa un patron SELECT-luego-INSERT-o-UPDATE. Esto funciona de forma fiable para
escenarios de escritor unico. Si necesitas upserts reales a nivel de base de datos para escrituras
concurrentes, considera usar `INSERT ... ON CONFLICT` especifico del dialecto via
`sqlalchemy.dialects.postgresql.insert` o `sqlalchemy.dialects.sqlite.insert`.

### Agregar filtros a `find_all()`

El diccionario `find_filters` se pasa desde la capa de casos de uso. Extiende la consulta con clausulas
WHERE basadas en las claves del filtro:

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

## Referencia

- Implementacion existente: `src/blog/infrastructure/storage/user_repository_sql.py`
- Definiciones de tablas: `src/blog/infrastructure/storage/sql_tables.py`
- Puerto SqlService: `src/shared/domain/services/sql_service.py`
- Implementacion SqlService: `src/shared/infrastructure/services/sql_service_sqlalchemy.py`
- Ejemplo de test: `tests/blog/infrastructure/storage/test_user_repository_sql.py`
