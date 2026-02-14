# Future Todo List

This document tracks planned improvements and missing implementations for the project.

## High Priority

- [ ] Implement Authentication and Authorization using OpenID with Authelia and Traefik.
- [ ] Create App Config
- [ ] Use App Factory to create MCP Server, HTTP Server and cli commands.

## Medium Priority

- [ ] Create Articles use case and related repository implementations.
- [ ] Use SQLAlchemy and Alembic for database interactions and migrations.
- [ ] Create SQL repository implementations for User and Article.
- [ ] Create MCP Server with FastMCP


## Low Priority

- [ ] Implement OpenTelemetry for tracing and monitoring.
- [ ] Implement LGTM stack
- [ ] Define rules for agents
- [ ] Create agents to generate components

## Completed

- [x] Implement error handlers to transform domain errors into HTTP errors (status code, error message).
- [x] Domain Events base classes (`shared/domain/events/`)
- [x] Event Types enum (`shared/domain/events/event_types.py`)
- [x] Password Service abstraction and implementations
- [x] User Creator use case
- [x] Memory and MongoDB repository implementations for User
- [x] Memory repository implementation for Article
