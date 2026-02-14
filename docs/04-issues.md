# Self-Similarity Issues

This document tracks architectural consistency issues identified in the codebase.

## Critical Issues

| Issue | Location | Description | Status |
|-------|----------|-------------|--------|
| ~~Typo~~ | ~~`user.py:39,51`~~ | ~~`crated_at` should be `created_at`~~ | ✅ Fixed |
| ~~Typo~~ | ~~`username_aready_exists.py`~~ | ~~Filename: "aready" should be "already"~~ | ✅ Fixed |
| ~~Missing inheritance~~ | ~~`user_deleter.py`~~ | ~~`UserDeleter` doesn't inherit `UseCase`~~ | ✅ Fixed |
| ~~Missing method~~ | ~~`article_repository_memory.py`~~ | ~~`find_by_slug()` not implemented~~ | ✅ Fixed |
| ~~Bug~~ | ~~`article_repository_memory.py:25`~~ | ~~`copy()` used incorrectly (imported as module)~~ | ✅ Fixed |
| ~~Mutable default~~ | ~~`user.py:36-37`~~ | ~~`following: List[str] = []` shared across instances~~ | ✅ Fixed |

## Pattern Inconsistencies

### Entities

| Category | User Pattern | Article Pattern | Issue | Status |
|----------|--------------|-----------------|-------|--------|
| ID generation | Internal (`uuid4()`) | External (parameter) | Should standardize | ❌ Open |
| Constructor | Direct assignment | `cls()` dataclass call | Different styles | ❌ Open |
| Return type on `create()` | Missing | `-> "Article"` | Inconsistent annotations | ❌ Open |

### Events

| Event | Payload Pattern | Issue | Status |
|-------|-----------------|-------|--------|
| `UserCreated` | None | Missing `user_id` | ❌ Open |
| `UserUpdated` | Untyped `payload` | Should be `user_id: str` | ❌ Open |
| `UserDeleted` | `user_id: str` | Correct | ✅ OK |
| Article events | `article_id: str` | Consistent | ✅ OK |

## Missing Implementations

### Use Cases

Declared in `__init__.py` but not implemented:

- `UserLogger` ❌
- `ArticleCreator` ❌
- `ArticleUpdater` ❌
- `ArticleDeleter` ❌

### Infrastructure

- `article_mapper.py` ❌
- `article_dtos.py` ❌
- `ArticleRepositoryMemory.clear()` method ❌

## Typos

| File | Typo | Correction | Status |
|------|------|------------|--------|
| ~~`user.py`, `user_dtos.py`, `user_mapper.py`, `test_user_creator.py`~~ | ~~`crated_at`~~ | ~~`created_at`~~ | ✅ Fixed |
| ~~`username_aready_exists.py`~~ | ~~filename~~ | ~~`username_already_exists.py`~~ | ✅ Fixed |
| ~~`user_not_following.py:4`~~ | ~~"becouse"~~ | ~~"because"~~ | ✅ Fixed |

## New Issues Discovered

| Issue | Location | Description |
|-------|----------|-------------|
| Missing return type | `user_creator.py:13` | `execute()` method missing return type annotation |
| Missing return type | `user_repository_memory.py:32` | `clear()` method missing `-> None` annotation |
| Signature mismatch | `article_repository_memory.py:24-26` | `find_all()` takes no args but interface requires `(find_filters, find_order, find_limits)` |
| Inconsistent import | `user_creator.py:1` | Uses `blog.domain.errors` instead of `src.blog.domain.errors` |
| Inconsistent import | `test_user_creator.py:8` | Uses `blog.domain.errors` instead of `src.blog.domain.errors` |

## What's Working Well

- Repository interfaces are consistent
- Domain events (for Article) follow a clean pattern
- Base classes (`DomainModel`, `DomainEvent`) provide good foundation
- Directory structure is well-organized per hexagonal architecture
- Password service implementations are consistent

## Summary

| Category | Fixed | Remaining |
|----------|-------|-----------|
| Critical Issues | 6 | 0 |
| Pattern Inconsistencies | 0 | 5 |
| Missing Implementations | 0 | 7 |
| Typos | 3 | 0 |
| New Issues | - | 5 |
| **Total** | **9** | **17** |
