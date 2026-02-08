# Future Todo List

This document tracks planned improvements and missing implementations for the project.

## High Priority

| Task                                | Description                                                                                                                                      |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Add `user_error_handlers.py`        | Implement error handlers to transform domain errors into HTTP errors (status code, error message). Currently error handling is inline in routes. |

## Medium Priority

| Task                          | Description                                                                                                |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Add shared domain errors      | Create a shared domain errors directory for base error classes that can be reused across bounded contexts. |
| Add article mappers           | Create mapper for Article entity similar to user_mapper.py.                                                |

## Low Priority

| Task                      | Description                                                                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Add Guards implementation | Implement authentication/authorization guards as mentioned in docs (checking if user is authenticated, has permissions, etc.).                    |
| Add External Services     | Implement external service integrations (email, payment, etc.) with abstract interfaces in domain and concrete implementations in infrastructure. |
| Add Application Services  | Implement application services for complex logic that spans multiple use cases.                                                                   |

## Completed

- [x] Domain Events base classes (`shared/domain/events/`)
- [x] Event Types enum (`shared/domain/events/event_types.py`)
- [x] Password Service abstraction and implementations
- [x] User Creator use case
- [x] Memory and MongoDB repository implementations for User
- [x] Memory repository implementation for Article
