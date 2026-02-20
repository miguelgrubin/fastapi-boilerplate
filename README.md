## Docker Development

Run the full stack with Traefik, Authelia, PostgreSQL, and Redis:

```bash
# Start all services
docker compose --env-file .env.docker up -d

# View logs
docker compose --env-file .env.docker logs -f

# Stop services
docker compose --env-file .env.docker down

# Clean up (removes volumes)
docker compose --env-file .env.docker down -v
```

### Initial Setup

1. **Start the stack:**
   ```bash
   docker compose --env-file .env.docker up -d
   ```

2. **Wait for services to be healthy:**
   ```bash
   docker compose --env-file .env.docker ps
   ```

3. **Access the services** (see table below)

### Access URLs

| Service | URL | Notes |
|---------|-----|-------|
| Traefik Dashboard | http://localhost:1081 | View routing configuration |
| Authelia | http://localhost:1080/auth | Login portal |
| FastAPI | http://localhost:1080/api | Protected API (redirects to login) |
| API Docs | http://localhost:1080/api/docs | OpenAPI documentation (public) |
| PostgreSQL | localhost:15432 | Direct database access |

**Authelia credentials:** admin / password

### How It Works

All routing is handled via path prefixes on `localhost:1080` using Traefik:

1. **Authelia Portal (`/auth`)**: Serves the authentication UI
2. **FastAPI API (`/api`)**: Protected by Authelia - unauthenticated requests redirect to `/auth`
3. **Public endpoints**: `/api/docs`, `/api/redoc`, `/api/openapi.json`, `/api/health` bypass authentication

The configuration follows the [Authelia + Traefik Setup Guide](https://www.authelia.com/blog/authelia--traefik-setup-guide/):

- `docker/traefik/config/traefik.yml` - Traefik static configuration
- `docker/traefik/config/dynamic.yml` - Middlewares for auth and path stripping
- `docker/authelia/config/configuration.yml` - Authelia settings with path-based access control
- `docker/authelia/config/users_database.yml` - User credentials

### Architecture

```
                    ┌─────────────────────────────────────────────────────┐
                    │                    Traefik                          │
                    │                  (Port 1080)                        │
                    └─────────────────────────────────────────────────────┘
                                           │
           ┌───────────────────────────────┼───────────────────────────────┐
           │                               │                               │
           ▼                               ▼                               ▼
    ┌─────────────┐               ┌─────────────────┐              ┌─────────────┐
    │   /auth/*   │               │  /api/docs etc  │              │   /api/*    │
    │  (bypass)   │               │    (bypass)     │              │ (protected) │
    └─────────────┘               └─────────────────┘              └─────────────┘
           │                               │                               │
           ▼                               │                               ▼
    ┌─────────────┐                        │                      ┌─────────────┐
    │  Authelia   │                        │                      │  Authelia   │
    │   Portal    │                        │                      │ ForwardAuth │
    └─────────────┘                        │                      └─────────────┘
                                           │                               │
                                           ▼                               ▼
                                    ┌─────────────────────────────────────────┐
                                    │              FastAPI App                │
                                    │              (Port 8000)                │
                                    └─────────────────────────────────────────┘
```

### Customization

**Change Authelia credentials:**
```bash
# Generate a new password hash
docker run authelia/authelia:latest authelia crypto hash generate argon2 --password 'your-password'

# Edit docker/authelia/config/users_database.yml with the new hash
```

**Generate secure secrets for production:**
```bash
# Generate new secrets
openssl rand -hex 32

# Update .env.docker with the generated values
```

---

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

### Type Checkers

- `ty`: Extremely fast Python type checker written in Rust. 10-100x faster than mypy with modern features like LSP support and advanced type narrowing.
- `pylint`: Checks code style to enforce PEP8, avoid code smells and suggest refactors.
<!-- - `radon`: Checks mantainability and cyclomatic complexity. -->

### Formatters

- `ruff`: Extremely fast Python linter and formatter. Replaces black and isort with 10-100x better performance.

<!-- ### Security Linters

- `safety`: Checks security vulnerabilities on dependencies.
- `bandit`: Checks security vulnerabilities scanning code statically. -->
