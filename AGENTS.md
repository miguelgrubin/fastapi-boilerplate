# AGENTS.md - Coding Agent Guidelines

This document provides guidelines for AI coding agents working in this FastAPI boilerplate repository.

## Project Overview

A FastAPI boilerplate using **Hexagonal Architecture** (Ports & Adapters) with Domain-Driven Design patterns.

- **Python**: 3.11+
- **Package Manager**: uv
- **Framework**: FastAPI with Pydantic
- **Architecture**: Hexagonal (Domain → Use Cases → Infrastructure)

## Build/Lint/Test Commands

### Installation

```bash
make install          # Install all dependencies (uv sync --all-extras)
make install-uv       # Install uv package manager
```

### Type Checking

ty is a fast, Rust-based type checker that replaces mypy. Key features:
- **10-100x faster** than mypy with excellent performance
- **Language server support** for IDE integration
- **Modern diagnostics** with comprehensive error messages
- **Configuration**: `[tool.ty]` in `pyproject.toml`

```bash
make typecheck        # Run ty type checker on src
uv run ty check src   # Run ty type checker (direct)
uv run ty check .     # Type check entire project
uv run ty check --watch  # Watch mode for development
```

For more information, see [ty documentation](https://docs.astral.sh/ty/).

### Testing

```bash
make test                              # Run all tests
uv run pytest tests                    # Run all tests (direct)
uv run pytest tests/path/to/test.py   # Run single test file
uv run pytest tests/path/to/test.py::test_function_name  # Run single test
uv run pytest tests -k "keyword"       # Run tests matching keyword
uv run pytest tests -v                 # Verbose output
uv run pytest tests --tb=short         # Shorter tracebacks
```

### Formatting & Linting

```bash
make format           # Auto-format code with ruff
make format-check     # Check formatting without modifying
make lint             # Run pylint
uv run ruff check .   # Run ruff linter
uv run ruff check --fix .  # Auto-fix ruff issues
```

### Running the Server

```bash
make start            # Start dev server with hot reload
```

## Project Structure

```
src/
├── app/
│   ├── blog/                    # Bounded context
│   │   ├── domain/              # Domain layer (entities, value objects, errors, events)
│   │   │   ├── errors/          # Domain exceptions
│   │   │   └── events/          # Domain events
│   │   ├── use_cases/           # Application layer (use cases/commands)
│   │   └── infrastructure/      # Infrastructure layer
│   │       ├── server/          # HTTP routes, DTOs
│   │       ├── storage/         # Repository implementations
│   │       └── mappers/         # Entity <-> DTO mappers
│   └── shared/                  # Shared kernel
│       ├── domain/              # Base domain classes
│       └── services/            # Shared services (e.g., PasswordService)
├── main.py                      # FastAPI app entrypoint
└── config.py                    # Configuration
tests/                           # Mirror src/ structure
```

## Code Style Guidelines

### Formatting

- **Line length**: 100 characters max
- **Quotes**: Double quotes (`"`)
- **Indentation**: 4 spaces
- **Formatter**: ruff (replaces black + isort)

### Import Order

Imports are organized in this order (enforced by ruff):
1. `__future__` imports
2. Type imports (`typing`, `types`, `typing_extensions`)
3. Standard library
4. Third-party packages
5. First-party (`app.*`)
6. Local folder

```python
from typing import List, Optional

from dataclasses import dataclass
from datetime import datetime

from fastapi import FastAPI

from app.blog.domain.user import User
```

### Type Annotations

- **All functions must have return type annotations** (enforced by ty)
- Use `Optional[T]` for nullable types
- Use `List[T]`, `Dict[K, V]` from `typing` module
- Use `TypedDict` for structured dictionaries
- Use `NoReturn` for functions that never return normally

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `UserCreator`, `UserRepository` |
| Functions/Methods | snake_case | `find_one`, `create_user` |
| Variables | snake_case | `user_id`, `password_hash` |
| Constants | UPPER_CASE | `USER_REPOSITORY`, `PASSWORD_SERVICE` |
| Modules | snake_case | `user_creator.py`, `user_repository.py` |
| Private | Leading underscore | `_users`, `_events` |

### Error Handling

- Create domain-specific exceptions in `domain/errors/`
- Exception classes inherit from `Exception`
- Include descriptive messages

```python
class UserAlreadyExits(Exception):
    def __init__(self):
        super().__init__("User with this username or email already exits.")
```

### Domain Models

- Inherit from `DomainModel` base class
- Use `@dataclass` for simple value objects
- Use factory methods (`create()`) for entity construction
- Record domain events using `self.record(DomainEvent)`

### Repositories

- Define abstract interface in `domain/` using `ABC`
- Implement concrete classes in `infrastructure/storage/`
- Name pattern: `{Entity}Repository` (interface), `{Entity}Repository{Impl}` (concrete)

### Use Cases

- One class per use case
- Constructor injection for dependencies
- Single `execute()` method as entry point
- Name pattern: `{Action}{Entity}` (e.g., `UserCreator`, `ArticleFinder`)

### DTOs and API Models

- Use Pydantic `BaseModel` for request/response DTOs
- Place in `infrastructure/server/` directory
- Name pattern: `{Entity}CreationDTO`, `{Entity}Response`

### Test Conventions

- Test files: `test_{module}.py`
- Test functions: `test_{description}`
- Use `pytest` fixtures and `unittest.mock` for mocking
- Mirror source structure in `tests/`

```python
def test_should_create_user_when_email_and_username_is_not_used():
    use_case = _create_new_use_case()
    user = use_case.execute("someone", "password", "someone@example.com")
    assert user.id != ""

@patch.object(UserRepositoryMemory, "save")
def test_should_save_on_repository(mock_save):
    use_case = _create_new_use_case()
    use_case.execute("someone", "password", "someone@example.com")
    mock_save.assert_called()
```

## Architecture Rules

1. **Domain layer has no external dependencies** - Only standard library and typing
2. **Use cases depend on domain interfaces** - Never on infrastructure
3. **Infrastructure implements domain interfaces** - Repositories, services
4. **Dependency injection via constructors** - No service locators
5. **Factory functions compose the application** - See `factory.py`
