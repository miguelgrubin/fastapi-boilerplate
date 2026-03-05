# Architectural Decision Record (Lite)

## ADR-001: Use Hexagonal Architecture

Context:
- Tight coupling between layers makes changes difficult and risky
- Framework/database changes directly affect business logic
- Difficulty testing business logic in isolation from infrastructure
- Code maintainability concerns as the project grows

Decision:
- Use Hexagonal Architecture (Ports & Adapters) to structure the application
- Domain layer has no external dependencies (only standard library)
- Use cases depend on domain interfaces (ports), never on infrastructure
- Infrastructure implements domain interfaces (adapters)
- Dependency injection via constructors, no service locators

Alternatives considered:
- Traditional Layered Architecture (Controller-Service-Repository): simpler but creates tight coupling between layers
- No formal architecture / Monolithic: fast to start but doesn't scale with team size or complexity

Trade-offs:
+ Clear separation of concerns between domain, application, and infrastructure
+ Business logic is framework-agnostic and easily testable
+ Infrastructure can be swapped without affecting domain (e.g., MongoDB to PostgreSQL)
+ Enforces dependency inversion, improving modularity
− More boilerplate code (interfaces, adapters, mappers)
− Steeper learning curve for developers unfamiliar with the pattern

Status:
- Accepted (2022-02-26)

## ADR-002: Use PostgreSQL + pgvector

Context:
- Application requires vector search capabilities for AI/ML features
- Need ACID transactions for data integrity

Decision:
- Use PostgreSQL as the primary relational database
- Use pgvector extension for vector similarity search and embeddings
- Use SQLAlchemy as the ORM layer
- Use asyncpg driver for async database connections
- Use Alembic for database migrations

Alternatives considered:
- Qdrant: Good vector search capabilities but adds operational complexity by requiring a separate system to manage

Trade-offs:
+ Single database for all needs (relational + vector)
+ Mature ecosystem with excellent documentation and community support
+ SQL-based vector queries using familiar syntax
+ Simplified operations with fewer moving parts
+ Data consistency without need for cross-system synchronization
− Requires PostgreSQL extension management overhead
− pgvector is newer technology, still evolving

Status:
- Proposed (2026-02-08)

## ADR-003: Use OAuth2 / OpenID Connect

Context:
- Avoid managing credentials and passwords internally
- Enterprise customers require SSO integration
- Must comply with security standards and best practices
- Multiple applications need shared authentication

Decision:
- Use Authelia as the OpenID Connect identity provider
- Validate JWTs issued by Authelia
- Integrate with FastAPI security dependencies
- Implement refresh token handling
- Implement RBAC via OIDC claims

Alternatives considered:
- Keycloak: Self-hosted but resource-heavy and complex to operate
- JWT-only (no IdP): Stateless tokens but lacks centralized identity management and SSO capabilities

Trade-offs:
+ Delegated credential management - no need to implement auth from scratch
+ Industry-standard protocols (OAuth2/OIDC)
+ Centralized identity management across multiple applications
− Requires additional infrastructure to deploy and maintain Authelia
− Protocol complexity with OAuth2/OIDC flows
− External dependency - authentication relies on Authelia availability

Status:
- Proposed (2026-02-08)
