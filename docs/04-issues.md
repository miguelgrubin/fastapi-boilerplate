# Self-Similarity Issues

This document tracks architectural consistency issues identified in the codebase.

## Critical Issues

All critical issues have been resolved. ✅

## Pattern Inconsistencies

### Entities

| Category                  | User Pattern         | Article Pattern      | Issue                    | Status   |
| ------------------------- | -------------------- | -------------------- | ------------------------ | -------- |
| ID generation             | Internal (`uuid4()`) | Internal (`uuid4()`) | Standardized             | ✅ Fixed |
| Constructor               | `cls()` dataclass    | `cls()` dataclass    | Standardized             | ✅ Fixed |
| Return type on `create()` | `-> "User"`          | `-> "Article"`       | Consistent annotations   | ✅ Fixed |

### Events

| Event         | Payload Pattern   | Issue                    | Status   |
| ------------- | ----------------- | ------------------------ | -------- |
| `UserCreated` | `user_id: str`    | Has user_id              | ✅ Fixed |
| `UserUpdated` | Untyped `payload` | Should be typed          | ❌ Open  |
| `UserDeleted` | `user_id: str`    | Correct                  | ✅ OK    |
| Article events| `article_id: str` | Consistent               | ✅ OK    |

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

All typos have been resolved. ✅

## Remaining Code Issues

| Issue               | Location                             | Description                                                                                 | Status   |
| ------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------- | -------- |
| ~~Missing return type~~ | ~~`user_creator.py:13`~~          | ~~`execute()` method missing return type annotation~~                                       | ✅ Fixed |
| ~~Missing return type~~ | ~~`user_repository_memory.py:32`~~| ~~`clear()` method missing `-> None` annotation~~                                           | ✅ Fixed |
| Signature mismatch  | `article_repository_memory.py:24-26` | `find_all()` takes no args but interface requires `(find_filters, find_order, find_limits)` | ❌ Open  |
| Inconsistent import | `user_creator.py:1`                  | Uses `blog.domain.errors` instead of `src.blog.domain.errors`                               | ❌ Open  |
| Inconsistent import | `test_user_creator.py:8`             | Uses `blog.domain.errors` instead of `src.blog.domain.errors`                               | ❌ Open  |

## What's Working Well

- Repository interfaces are consistent
- Domain events (for Article) follow a clean pattern
- Base classes (`DomainModel`, `DomainEvent`) provide good foundation
- Directory structure is well-organized per hexagonal architecture
- Password service implementations are consistent
- Entity patterns now standardized (ID generation, constructors, return types)

## Summary

| Category                | Fixed  | Remaining |
| ----------------------- | ------ | --------- |
| Critical Issues         | 6      | 0         |
| Pattern Inconsistencies | 4      | 1         |
| Missing Implementations | 0      | 7         |
| Typos                   | 3      | 0         |
| Code Issues             | 2      | 3         |
| **Total**               | **15** | **11**    |

## Remaining Issues Checklist

- [ ] `UserUpdated` event - type the `payload` parameter
- [ ] `UserLogger` use case
- [ ] `ArticleCreator` use case
- [ ] `ArticleUpdater` use case
- [ ] `ArticleDeleter` use case
- [ ] `article_mapper.py`
- [ ] `article_dtos.py`
- [ ] `ArticleRepositoryMemory.clear()` method
- [ ] `find_all()` signature mismatch in `article_repository_memory.py`
- [ ] Inconsistent import in `user_creator.py:1`
- [ ] Inconsistent import in `test_user_creator.py:8`
