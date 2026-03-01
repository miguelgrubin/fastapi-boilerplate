# Future Todo List

This document tracks planned improvements and missing implementations for the project.

## High Priority

- [x] Implement Authentication and Authorization using OpenID with Authelia and Traefik.
- [ ] Use App Factory to create MCP Server, HTTP Server and CLI commands.

## Medium Priority

- [x] Create Articles use case and related repository implementations.
- [x] Use SQLAlchemy and Alembic for database interactions and migrations.
- [ ] Create SQL repository implementations for User and Article.
- [ ] Create MCP Server with FastMCP
- [x] Create HTTP Server with FastAPI
- [ ] Create CLI commands for create and list users.

## Low Priority

- [ ] Implement OpenTelemetry for tracing and monitoring.
- [ ] Implement LGTM stack
- [ ] Define rules for agents
- [ ] Create agents to generate components

## Completed

- [x] Create App Settings
- [x] Implement error handlers to transform domain errors into HTTP errors (status code, error message).
- [x] Domain Events base classes (`shared/domain/events/`)
- [x] Event Types enum (`shared/domain/events/event_types.py`)
- [x] Password Service abstraction and implementations
- [x] User Creator use case
- [x] Memory and MongoDB repository implementations for User
- [x] Memory repository implementation for Article
