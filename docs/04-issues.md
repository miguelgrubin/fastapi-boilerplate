# Self-Similarity Issues

This document tracks architectural consistency issues identified in the codebase.

## Critical Issues

| Issue | Location | Description |
|-------|----------|-------------|
| Typo | `user.py:39,51` | `crated_at` should be `created_at` |
| Typo | `username_aready_exists.py` | Filename: "aready" should be "already" |
| Missing inheritance | `user_deleter.py` | `UserDeleter` doesn't inherit `UseCase` |
| Missing method | `article_repository_memory.py` | `find_by_slug()` not implemented |
| Bug | `article_repository_memory.py:25` | `copy()` used incorrectly (imported as module) |
| Mutable default | `user.py:36-37` | `following: List[str] = []` shared across instances |

## Pattern Inconsistencies

### Entities

| Category | User Pattern | Article Pattern | Issue |
|----------|--------------|-----------------|-------|
| ID generation | Internal (`uuid4()`) | External (parameter) | Should standardize |
| Constructor | Direct assignment | `cls()` dataclass call | Different styles |
| Return type on `create()` | Missing | `-> "Article"` | Inconsistent annotations |

### Events

| Event | Payload Pattern | Issue |
|-------|-----------------|-------|
| `UserCreated` | None | Missing `user_id` |
| `UserUpdated` | Untyped `payload` | Should be `user_id: str` |
| `UserDeleted` | `user_id: str` | Correct |
| Article events | `article_id: str` | Consistent |

## Missing Implementations

### Use Cases

Declared in `__init__.py` but not implemented:

- `UserLogger`
- `ArticleCreator`
- `ArticleUpdater`
- `ArticleDeleter`

### Infrastructure

- `article_mapper.py`
- `article_dtos.py`
- `ArticleRepositoryMemory.clear()` method

## Typos

| File | Typo | Correction |
|------|------|------------|
| `user.py`, `user_dtos.py`, `user_mapper.py`, `test_user_creator.py` | `crated_at` | `created_at` |
| `username_aready_exists.py` | filename | `username_already_exists.py` |
| `user_not_following.py:4` | "becouse" | "because" |

## What's Working Well

- Repository interfaces are consistent
- Domain events (for Article) follow a clean pattern
- Base classes (`DomainModel`, `DomainEvent`) provide good foundation
- Directory structure is well-organized per hexagonal architecture
- Password service implementations are consistent
