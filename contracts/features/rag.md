# RAG with pgvector - Implementation Plan

## Overview

Implement Retrieval-Augmented Generation (RAG) capabilities using pgvector for semantic similarity search. This enables context-aware article and comment retrieval based on semantic similarity rather than keyword matching.

## Technologies

- **LangChain**: For embeddings pipeline and vector store orchestration
- **pgvector**: PostgreSQL extension for vector similarity search
- **langchain-postgres**: Provides `PGVectorStore` for database integration
- **langchain-core**: Core abstractions for embeddings and LLM interactions
- **langchain-cohere**: Cohere embeddings provider (or alternative embedding service)
- **SQLAlchemy**: ORM for database operations

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 RAG Infrastructure Layer                 │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │        Embedding Service (LangChain)            │   │
│  │  - Cohere Embeddings (or alternative)           │   │
│  │  - Lazy loading via dependency injection        │   │
│  └──────────────────────────────────────────────────┘   │
│                           │                               │
│                           ▼                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │       Article Vector Store (pgvector)           │   │
│  │  - PGVectorStore from langchain-postgres        │   │
│  │  - Fields: title, description, content, tags    │   │
│  └──────────────────────────────────────────────────┘   │
│                           │                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │        Comment Vector Store (pgvector)          │   │
│  │  - PGVectorStore from langchain-postgres        │   │
│  │  - Field: content                               │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │     Repository Similarity Search Methods        │   │
│  │  - ArticleRepositorySql.similarity_search()     │   │
│  │  - CommentRepositorySql.similarity_search()     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Implementation Tasks

### Phase 1: Database Schema Enhancement

#### 1.1 Update Article Table Schema
- Add `embedding` column of type `vector(1536)` to `articles_table`
- Column should be nullable initially (backfill existing records)
- Add index: `CREATE INDEX ON articles USING ivfflat (embedding vector_cosine_ops)`

**Location**: `src/blog/infrastructure/storage/sql_tables.py`

**Changes**:
```python
# In the articles table definition:
# - Add: embedding = Column(Vector(1536), nullable=True)
# - Add: Index for vector similarity search
```

#### 1.2 Update Comment Table Schema
- Add `embedding` column of type `vector(1536)` to `comments_table`
- Column should be nullable initially (backfill existing records)
- Add index: `CREATE INDEX ON comments USING ivfflat (embedding vector_cosine_ops)`

**Location**: `src/blog/infrastructure/storage/sql_tables.py`

**Changes**:
```python
# In the comments table definition:
# - Add: embedding = Column(Vector(1536), nullable=True)
# - Add: Index for vector similarity search
```

#### 1.3 Create Migration Scripts
- Create Alembic migration to add embedding columns
- Create data migration to seed embeddings for existing records

**Location**: `migrations/versions/`

### Phase 2: Embedding Service Implementation

#### 2.1 Create Embedding Service
- New module: `src/shared/infrastructure/embeddings/embedding_service.py`
- Abstraction: Define `EmbeddingService` interface in domain layer
- Implementation: Wrap LangChain `Embeddings` with Cohere provider
- Handle API errors and rate limiting

**Responsibilities**:
- Lazy load embeddings to avoid unnecessary initialization
- Batch embed documents for efficiency
- Cache embeddings for repeated text

**Interface**:
```python
class EmbeddingService(ABC):
    async def embed_text(self, text: str) -> List[float]: ...
    async def embed_texts(self, texts: List[str]) -> List[List[float]]: ...
```

#### 2.2 Configure Embeddings
- Add configuration in `src/config.py`:
  - `COHERE_API_KEY` (from environment)
  - `EMBEDDING_MODEL` (default: "embed-english-v3.0")
  - `EMBEDDING_DIMENSION` (1536 for Cohere)
- Add `.env` entry for configuration

### Phase 3: Vector Store Integration

#### 3.1 Create Article Vector Store Factory
- New module: `src/blog/infrastructure/storage/article_vector_store.py`
- Factory function to create `PGVectorStore` for articles
- Configuration:
  - Collection name: `"articles"`
  - Fields to embed:
    - `title` (weight: high - semantic importance)
    - `description` (weight: medium)
    - `content` (weight: high - primary search target)
    - `tags` (weight: medium - metadata relevance)
  - Combined embedding strategy: concatenate fields with separators

**Implementation**:
```python
def create_article_vector_store(
    embedding_service: EmbeddingService,
    sql_service: SqlService,
) -> PGVectorStore: ...
```

#### 3.2 Create Comment Vector Store Factory
- New module: `src/blog/infrastructure/storage/comment_vector_store.py`
- Factory function to create `PGVectorStore` for comments
- Configuration:
  - Collection name: `"comments"`
  - Field to embed: `content`

**Implementation**:
```python
def create_comment_vector_store(
    embedding_service: EmbeddingService,
    sql_service: SqlService,
) -> PGVectorStore: ...
```

#### 3.3 Update Document Synchronization
- Hook into repository `save()` methods
- Auto-generate and store embeddings when documents are saved/updated
- Lazy loading: Only compute embeddings if embedding service is available

### Phase 4: Similarity Search Methods

#### 4.1 ArticleRepositorySql Enhancement

**New Method**: `similarity_search()`
```python
def similarity_search(
    self,
    query: str,
    top_k: int = 5,
    score_threshold: float = 0.0,
) -> List[Tuple[Article, float]]:
    """
    Search articles by semantic similarity.
    
    Args:
        query: Search query text
        top_k: Number of results to return
        score_threshold: Minimum similarity score (0-1)
        
    Returns:
        List of (Article, similarity_score) tuples, ordered by relevance
        
    Raises:
        EmbeddingServiceError: If embedding generation fails
    """
    ...
```

**Implementation Details**:
- Use `PGVectorStore.similarity_search_with_score()`
- Embed the query using the same embedding service
- Execute cosine similarity search via pgvector
- Map results back to Article domain entities
- Return tuples of (Article, similarity_score)

**Location**: `src/blog/infrastructure/storage/article_repository_sql.py`

#### 4.2 CommentRepositorySql Enhancement

**New Method**: `similarity_search()`
```python
def similarity_search(
    self,
    query: str,
    article_id: Optional[str] = None,
    top_k: int = 5,
    score_threshold: float = 0.0,
) -> List[Tuple[Comment, float]]:
    """
    Search comments by semantic similarity.
    
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
    ...
```

**Implementation Details**:
- Use `PGVectorStore.similarity_search_with_score()`
- Optionally filter by `article_id` using SQLAlchemy WHERE clause
- Embed the query using the same embedding service
- Execute cosine similarity search via pgvector
- Map results back to Comment domain entities
- Return tuples of (Comment, similarity_score)

**Location**: `src/blog/infrastructure/storage/comment_repository_sql.py`

### Phase 5: Use Case Integration

#### 5.1 Create Search Use Cases
- New use case: `SearchArticlesUseCase` 
  - Orchestrates article similarity search
  - Takes query string, returns ranked articles
  - Location: `src/blog/use_cases/search_articles.py`

- New use case: `SearchCommentsUseCase`
  - Orchestrates comment similarity search
  - Supports filtering by article
  - Location: `src/blog/use_cases/search_comments.py`

**Signatures**:
```python
class SearchArticlesUseCase:
    def __init__(self, article_repository: ArticleRepository): ...
    def execute(self, query: str, top_k: int = 5) -> List[SearchResult]: ...

class SearchCommentsUseCase:
    def __init__(self, comment_repository: CommentRepository): ...
    def execute(
        self, 
        query: str, 
        article_id: Optional[str] = None, 
        top_k: int = 5
    ) -> List[SearchResult]: ...
```

#### 5.2 Create API Endpoints
- New endpoint: `POST /api/articles/search`
  - Request: `{"query": "...", "top_k": 5}`
  - Response: List of articles with similarity scores

- New endpoint: `POST /api/articles/{article_id}/comments/search`
  - Request: `{"query": "...", "top_k": 5}`
  - Response: List of comments with similarity scores

**Location**: `src/blog/infrastructure/server/api_routes.py`

### Phase 6: Testing & Validation

#### 6.1 Unit Tests
- Test embedding service with mock Cohere API
- Test vector store creation and configuration
- Test similarity_search() methods with mock embeddings
- Test embedding caching and batching

**Location**: `tests/blog/infrastructure/storage/`

#### 6.2 Integration Tests
- Full pipeline: Create article → Generate embedding → Search
- Full pipeline: Create comment → Generate embedding → Search
- Test filtering by article_id for comments
- Test similarity score ordering

#### 6.3 Performance Tests
- Benchmark similarity search latency
- Test with realistic document volumes (100+, 1000+)
- Validate vector index efficiency

## Dependencies to Add

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project.optional-dependencies]
rag = [
    "langchain>=0.2.0",
    "langchain-core>=0.2.0",
    "langchain-postgres>=0.1.0",
    "langchain-cohere>=0.1.0",
    "cohere>=5.0.0",
    "pgvector>=0.1.0",
    "sqlalchemy>=2.0.0",
]
```

## Configuration Example

```python
# src/config.py

class Settings(BaseSettings):
    # ... existing settings ...
    
    # RAG/Vector Search Configuration
    EMBEDDINGS_ENABLED: bool = Field(
        default=False,
        description="Enable embeddings and vector search"
    )
    COHERE_API_KEY: str = Field(
        default="",
        description="Cohere API key for embeddings"
    )
    EMBEDDING_MODEL: str = Field(
        default="embed-english-v3.0",
        description="Cohere embedding model"
    )
    EMBEDDING_DIMENSION: int = Field(
        default=1536,
        description="Embedding vector dimension"
    )
    SIMILARITY_THRESHOLD: float = Field(
        default=0.5,
        description="Minimum similarity score for search results"
    )
```

## Implementation Order

1. **Database Schema** (Phase 1)
2. **Embedding Service** (Phase 2)
3. **Vector Store Factories** (Phase 3)
4. **Repository Methods** (Phase 4)
5. **Use Cases & API** (Phase 5)
6. **Tests** (Phase 6)

## Rollout Strategy

### Stage 1: Infrastructure (Feature Flag Disabled)
- Database migrations deployed
- Embedding service implemented
- Vector stores configured
- **No production impact** - disabled by default

### Stage 2: Data Seeding
- Backfill embeddings for existing articles and comments
- Validate embedding quality
- Monitor PostgreSQL disk usage

### Stage 3: Gradual Rollout
- Enable in development environment
- Enable in staging with monitoring
- Canary deployment to production (10% traffic)
- Full production rollout

### Stage 4: Optimization
- Monitor search latency
- Tune vector index parameters
- Implement caching if needed

## Error Handling

### Embedding Service Errors
- Cohere API timeout → Fallback to keyword search
- Rate limiting → Queue and retry with backoff
- Invalid API key → Log error, disable embeddings

### Vector Search Errors
- pgvector extension not installed → Graceful degradation
- Missing embeddings → Skip similarity search
- Database connection errors → Standard retry logic

## Monitoring & Observability

### Metrics to Track
- Embedding generation latency
- Similarity search latency (p50, p95, p99)
- Cache hit rate for embeddings
- Cohere API error rate and quota usage

### Logs to Capture
- Embedding generation requests/responses
- Search queries and result counts
- Performance outliers
- Error conditions and fallbacks

## Future Enhancements

1. **Hybrid Search**: Combine vector similarity with keyword matching
2. **Embeddings Caching**: Redis cache for frequently embedded texts
3. **Multiple Embedding Models**: Support OpenAI, Hugging Face alternatives
4. **Batch Embeddings**: Async background job for backfilling
5. **Search Analytics**: Track popular search queries and click-through rates
6. **Reranking**: Use LLM to rerank similarity search results
7. **Semantic Clustering**: Group related articles using embeddings
8. **Query Expansion**: Enhance queries with related terms before search

## References

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [LangChain Documentation](https://python.langchain.com/)
- [LangChain PostgreSQL Integration](https://python.langchain.com/docs/integrations/vectorstores/pgvector)
- [Cohere Embeddings API](https://docs.cohere.com/reference/embed)
