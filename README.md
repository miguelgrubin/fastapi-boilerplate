## Docker Development

Run the full stack with Nginx Proxy Manager, Authelia, PostgreSQL (pgvector), and Redis:

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

2. **Access Nginx Proxy Manager Admin UI:**
   - URL: http://localhost:81
   - Default login: `admin@example.com` / `changeme`
   - You'll be prompted to change credentials on first login

3. **Configure Proxy Host in NPM:**

   Create a single proxy host for `localhost` with path-based routing:

   - **Details tab:**
     - Domain Names: `localhost`
     - Scheme: `http`
     - Forward Hostname/IP: `127.0.0.1` (placeholder, actual routing is in Advanced)
     - Forward Port: `80` (placeholder)
     - Enable "Block Common Exploits"

   - **Advanced tab:**
     - Copy and paste the entire contents of `docker/nginx-proxy-manager/path-routing.conf`

   This configures:
   - `/auth/*` → Authelia portal
   - `/api/*` → FastAPI (protected by Authelia, prefix stripped)
   - `/` → Redirects to `/api/docs`

### Access URLs

| Service | URL | Notes |
|---------|-----|-------|
| NPM Admin | http://localhost:81 | Configure proxy hosts here |
| Authelia | http://localhost/auth | Login portal |
| FastAPI | http://localhost/api | Protected API (redirects to /api/docs) |
| API Docs | http://localhost/api/docs | OpenAPI documentation |
| PostgreSQL | localhost:5432 | Direct database access |

**Authelia credentials:** admin / password

### How It Works

All routing is handled via path prefixes on a single `localhost` domain:

1. **Authelia Portal (`/auth`)**: Serves the authentication UI
2. **FastAPI API (`/api`)**: Protected by Authelia - unauthenticated requests redirect to `/auth`
3. **Public endpoints**: `/api/docs`, `/api/redoc`, `/api/openapi.json`, `/api/health` bypass authentication

The Nginx configuration in `docker/nginx-proxy-manager/path-routing.conf`:
- Routes requests based on path prefix
- Strips `/api` prefix before forwarding to FastAPI
- Handles Authelia forward-auth verification
- Passes authenticated user info to FastAPI via headers (`Remote-User`, `Remote-Email`, etc.)

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
