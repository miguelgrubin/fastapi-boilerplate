# Introduction

**What?**

Its a blog example using hexagonal architecture using app modules. Oriented to Large Projects.

**Why?**

_Why Hexagonal Architecture?_

Ports and Adapters, decoupled, testing strategy, tracing errors. ToDo: Explain this

**How?**

```
Layers            || Components     || Testing Strategy
=========================================================================================
Presentation      || HTTP Routing   || Integration && E2E tests
 ↓ ↑              ||                ||
Application       || Use Cases      || Social Unit Testing (Use Cases + Domain)
 ↓ ↑              ||                ||
Domain            || Domain Models  || Solitary Unit Testing (single class or function)
 ↓ ↑              ||                ||
Infrastructure    || Repositories   || Integration testing
```

## Project Schema

```
src
├── app
│   ├── blog
│   │   ├── application
│   │   │   └── use_cases                       <=  Use Cases
│   │   │       ├── __init__.py
│   │   │       ├── user_creator.py
│   │   │       └── user_logger.py
│   │   ├── domain
│   │   │   ├── article.py                      <=  Article Domain Model
│   │   │   ├── article_repository.py           <=  Article Abstract Repository
│   │   │   ├── errors                          <=  Blog Domain Errors (UserNotFound, UserAlreadyExits, ...)
│   │   │   ├── events                          <=  Blog Domain Events (ArticleCreated, UserFollowed, ...)
│   │   │   ├── event_types.py                  <=  Enum with all event types on Blog
│   │   │   ├── user.py                         <=  User Domain Model
│   │   │   └── user_repository.py              <=  User Abstract Repository
│   │   ├── factory.py                          <=  Factories to initialize a Blog module (server, services, repositories, ...)
│   │   ├── infrastructure
│   │   │   ├── mappers                         <=  Mappers to transform (DTO <=> Domain Model <=> ORM Model)
│   │   │   │   └── user_mapper.py
│   │   │   ├── server                          <=  HTTP Routing
│   │   │   │   ├── article_routes.py           <=  Article Routing
│   │   │   │   ├── user_dtos.py                <=  User DTO (Requests, responses, query args)
│   │   │   │   ├── user_error_handlers.py      <=  Error handling (DomainError => HTTP Error)
│   │   │   │   └── user_routes.py              <=  User Routing
│   │   │   └── storage                         <=  Repository Implementations
│   │   │       ├── article_repository_memory.py
│   │   │       ├── article_repository_mongodb.py
│   │   │       ├── user_repository_memory.py
│   │   │       └── user_repository_mongodb.py
│   │   └── types.py                            <=  Blog typing objects
│   └── shared                                  <=  Shared Module
│       ├── application
│       │   └── use_case.py                     <=  Base UseCase definition
│       ├── domain
│       │   ├── errors                          <=  Shared Domain Error
│       │   ├── events                          <=  Shared Domain Events
│       │   ├── services                        <=  Shared Abstract Services
│       ├── factory.py                          <=  Factories to initialize Shared module
│       ├── infrastructure
│       │   └── services                        <=  Shared Implemented Services
│       └── types.py                            <=  Shared Typing
├── config.py                                   <=  App Config
├── factories.py                                <=  Factories to initialize an App instance
└── main.py                                     <=  Entrypoint
```

## Infrastructure Layer

- **Server**: They are responsible to expose the application to the outside world. In this example we have an HTTP Server implemented with FastAPI, but it could be a gRPC server or even MCP Servers.
- **Storage**: They are responsible to persist and retrieve data from the database. They implement the abstract repositories defined on the Domain Layer. In this example we have two implementations for each repository: in-memory and MongoDB.
- **Services**: They are responsible to interact with external services (email, payment, ...).

### HTTP Server Components

- **Routers**: FastAPI APIRouter with the HTTP endpoints.
- **DTOs**: Data Transfer Objects. Pydantic models to define the shape of the data on the HTTP layer (requests, responses, query args, ...).
- **Error Handlers**: Functions to transform Domain Errors into HTTP Errors (status code, error message, ...).
- **Guards**: Functions to check preconditions before execute a Use Case (Is the user authenticated? Does the user have permissions to execute this action? ...). ToDo: Not implemented yet.

### Storage Components (Repositories)

They are responsible to persist and retrieve data from the database. They implement the abstract repositories defined on the Domain Layer. In this example we have two implementations for each repository: in-memory and MongoDB.

### External Services

They are responsible to interact with external services (email, payment, ...). They implement the abstract services defined on the Shared Domain Layer. ToDo: Not implemented yet.

## Application Layer

- **Use Cases**: They are responsible to execute the business logic of the application. They interact with the Domain Layer to execute the business rules and with the Infrastructure Layer to persist data or interact with external services. They are the main component of the Application Layer and the only one that should be tested with Social Unit Testing (Use Cases + Domain). ToDo: Explain why.

## Domain Layer

- **Domain Models**: They are the main component of the Domain Layer. They represent the main entities of the application (User, Article, ...). They contain the business rules and logic of the application. They should be tested with Solitary Unit Testing (single class or function) to ensure that the business rules are correctly implemented. ToDo: Explain why.
- **Abstract Repositories**: They are interfaces that define the methods to persist and retrieve data from the database. They are implemented by the Storage components of the Infrastructure Layer.
- **Domain Errors**: They are custom exceptions that represent the errors that can occur in the Domain Layer (UserNotFound, UserAlreadyExits, ...). They are used to handle errors in the Use Cases and to transform them into HTTP Errors in the Error Handlers of the Server.
- **Domain Events**: They are events that represent something that has happened in the Domain Layer (ArticleCreated, UserFollowed, ...). They can be used to trigger actions in the application (send an email when a user is created, ...). ToDo: Not implemented yet.
