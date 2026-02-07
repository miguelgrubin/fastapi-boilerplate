## Main Dependencies

- `uvicorn`: Asynchronous web server interface, similar to `rack` on Ruby.
- `fastapi`: Asynchronous typed web framwork that generates openapi specs based on types.
- `pydantic`: Validator/Serializer based on typed Python and `dataclasses`.
- `typer`: Terminal library to create easy cli command based on types, generating autocompletes and `--help`.
- `rich`: Terminal library to generate beautiful output on cli.
<!-- - `sqlalchemy`: SQL ORM that implements data-mapper (similar to Hibernate on Java) but also active record (similar to ActiveRecord on Rails).
- `alembic`: Database migration tool for SQLAlchemy. -->
- `arrow`: Library to manage datetimes easily.
<!-- - `dependency-injector`: Library to use dependency injection using types signature. -->
- `pwdlib`: Modern password hashing library (Argon2).
- `python-jose[cryptography]`: Library to JavaScript Object Signing and Encryption (JOSE) = JWS + JWE + JWK + JWA + JWT
- `aiohttp`: Async client for http

## Testing Dependencies

- `pytest`: Testing framework and runner, 100% compatible with native `unittesting` framework and `nosetest`.
- `faker`: Library to generate fake data.
<!-- - `factory_boy`: Library to generate factory models for many Python ORMs. Inspired by `factory_bot` on Ruby. -->
- `coverage`: Tool to generate coverage reports using `pytests`, native `unittesting` or `nosetest`.
<!-- - `tox`: Testing automation framework to run tests across many python version and environments. -->

## Development Tooling

### Environment

<!-- - `pyenv`: Python version manager. Similar to `nvm` on NodeJS and `rbenv` on Ruby. -->

- `uv`: Fast Python package installer and resolver. Manages dependencies and virtual environments. Similar to `npm` on NodeJS but significantly faster.

### Documentation

- `mkdocs`: Generates HTML help pages from markdowns stored on `docs`.
- `mkdocs-material`: Material theme for `mkdocs`.

### Linters

- `mypy`: Checks types integrity.
- `pylint`: Checks code style to enforce PEP8, avoid code smells and suggest refactors.
<!-- - `radon`: Checks mantainability and cyclomatic complexity. -->

### Formatters

- `ruff`: Extremely fast Python linter and formatter. Replaces black and isort with 10-100x better performance.

<!-- ### Security Linters

- `safety`: Checks security vulnerabilities on dependencies.
- `bandit`: Checks security vulnerabilities scanning code statically. -->
