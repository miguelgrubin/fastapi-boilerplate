
## Requirements
- Python 3.12+
- Docker (for development)
- OpenSSL (for generating secrets)
- uv (for managing dependencies and virtual environments)
- mkcert (for generating local TLS certificates)

## Available Commands

### Setup

| Command | Description |
|---------|-------------|
| `make install-uv` | Install the uv package manager |
| `make install` | Install all dependencies (`uv sync --all-extras`) |

### Development

| Command | Description |
|---------|-------------|
| `make start` | Start the development server with hot reload |
| `make start-debug` | Start the development server with debugpy listening on `0.0.0.0:5678` |
| `make format` | Auto-format code with ruff |
| `make format-check` | Check formatting without modifying files |
| `make lint` | Run pylint on source code |
| `make typecheck` | Run ty type checker on `src/` |


### Testing

| Command | Description |
|---------|-------------|
| `make test` | Run all tests with pytest |
| `make coverage` | Run tests and display coverage report |
| `make coverage-html` | Run tests and generate HTML coverage report in `htmlcov/` |

### Database

| Command | Description |
|---------|-------------|
| `make migrate` | Apply all pending migrations (`alembic upgrade head`) |
| `make migrate-create m="description"` | Generate a new migration from model changes |
| `make migrate-downgrade` | Rollback the last migration |
| `make migrate-history` | Show migration history |

### Documentation

| Command | Description |
|---------|-------------|
| `make docs` | Build documentation for all languages (EN + ES) |
| `make docs-serve` | Serve English documentation locally at `http://127.0.0.1:8000` |
| `make docs-serve-es` | Serve Spanish documentation locally at `http://127.0.0.1:8000` |

### Docker Services (PostgreSQL, Redis, Authelia, Traefik)

| Command | Description |
|---------|-------------|
| `make docker-services-up` | Start PostgreSQL, Redis, Authelia, and Traefik |
| `make docker-services-down` | Stop all services |
| `make docker-services-ps` | List running services |
| `make docker-services-logs` | View service logs |
| `make docker-services-clean` | Stop services and remove volumes |

### Docker Full Stack (Services + FastAPI App)

| Command | Description |
|---------|-------------|
| `make docker-dev-up` | Start services and FastAPI app |
| `make docker-dev-down` | Stop everything |
| `make docker-dev-ps` | List all containers |
| `make docker-dev-logs` | View app logs |
| `make docker-dev-logs-all` | View all logs |
| `make docker-dev-rebuild` | Rebuild and start everything |
| `make docker-dev-clean` | Stop everything and remove volumes |

### Database Access

| Command | Description |
|---------|-------------|
| `make docker-db-connect` | Connect to PostgreSQL database |
| `make docker-redis-connect` | Connect to Redis CLI |
| `make docker-app-shell` | Open shell in app container |

### Infrastructure

| Command | Description |
|---------|-------------|
| `make certs` | Generate local TLS certificates with mkcert |
| `make clean` | Remove all build artifacts, caches, and temporary files |

## Docker Development

Run the full stack with Traefik, Authelia, PostgreSQL, and Redis using make commands:

```bash
# Start all services
make docker-services-up

# Start services + FastAPI app (recommended)
make docker-dev-up

# View logs
make docker-dev-logs-all

# Stop everything
make docker-dev-down

# Clean up (removes volumes)
make docker-dev-clean
```

Or use docker compose directly:

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
| Traefik Dashboard | http://localhost:8080 | View routing configuration |
| Authelia | http://auth.localtest.me | Login portal |
| FastAPI | http://blog.localtest.me | API with OIDC auth (login via `/auth/login`) |
| API Docs | http://blog.localtest.me/docs | OpenAPI documentation (public) |
| PostgreSQL | localhost:15432 | Direct database access |
| FastAPI (Local) | http://localhost:8000 | Direct API access (when using `make start` or `make start-debug`) |

**Authelia credentials:** admin / password

### Debugging

You can debug this application using `debugpy` in several editors and IDEs. It is automatically enabled and listening on `0.0.0.0:5678` when you run `make start-debug` or `docker-dev-up`.

To attach a debugger from:

- *VSCode*: Use the "Python: Remote Attach" configuration in `launch.json` with host `localhost` and port `5678`.
- *Neovim*: Use the `nvim-dap` plugin with a similar remote attach configuration. [Read this guide](https://codeberg.org/mfussenegger/nvim-dap/wiki/Debug-Adapter-installation#python).
- *PyCharm*: Use the "Python Remote Debug" configuration with host `localhost` and port `5678`.
- *Zed*: Press **F4** and select **"FastAPI: Attach to Remote Debugger (0.0.0.0:5678)"**

### How It Works

All routing is handled via subdomains on `*.localtest.me` using Traefik:

1. **Authelia (`auth.localtest.me`)**: OpenID Connect 1.0 Provider (identity provider)
2. **FastAPI (`blog.localtest.me`)**: OIDC Relying Party via Authlib, with PyCasbin RBAC on all endpoints
3. **Auth flow**: `GET /auth/login` -> Authelia login -> `/auth/callback` -> session created -> API access checked by Casbin

Key config files:

- `docker/traefik/config/traefik.yml` - Traefik static configuration
- `docker/authelia/config/configuration.yml` - Authelia settings with OIDC provider config
- `docker/authelia/config/users_database.yml` - User credentials
- `src/config/casbin_model.conf` - RBAC model definition
- `src/config/casbin_policy.conf` - Role and permission policies

### Architecture

```
User -> Traefik (Port 80)
           ├── auth.localtest.me -> Authelia (OIDC Provider)
           └── blog.localtest.me -> FastAPI (Port 8000)
                                       ├── /auth/* (Authlib OIDC client)
                                       │      login -> Authelia -> callback -> session
                                       └── /app/*, /admin/* (protected)
                                              └── PyCasbin RBAC (groups -> roles -> permissions)
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
- `sqlalchemy`: SQL ORM that implements data-mapper (similar to Hibernate on Java) but also active record (similar to ActiveRecord on Rails).
- `alembic`: Database migration tool for SQLAlchemy.
- `arrow`: Library to manage datetimes easily.
- `pwdlib`: Modern password hashing library (Argon2).
- `aiohttp`: Async client for http
- `authlib`: OpenID Connect / OAuth 2.0 client (OIDC Relying Party)
- `casbin`: PyCasbin RBAC authorization engine
- `httpx`: HTTP client required by Authlib's async Starlette integration
- `itsdangerous`: Required by Starlette `SessionMiddleware` for signed cookies

## Testing Dependencies

- `pytest`: Testing framework and runner, 100% compatible with native `unittesting` framework and `nosetest`.
- `faker`: Library to generate fake data.
- `coverage`: Tool to generate coverage reports using `pytests`, native `unittesting` or `nosetest`.

## Development Tooling

### Environment

- `uv`: Fast Python package installer and resolver. Manages dependencies and virtual environments. Similar to `npm` on NodeJS but significantly faster.

### Documentation

- `mkdocs`: Generates HTML help pages from markdowns stored on `docs`.
- `mkdocs-material`: Material theme for `mkdocs`.

### Type Checkers

- `ty`: Extremely fast Python type checker written in Rust. 10-100x faster than mypy with modern features like LSP support and advanced type narrowing.
- `pylint`: Checks code style to enforce PEP8, avoid code smells and suggest refactors.

### Formatters

- `ruff`: Extremely fast Python linter and formatter. Replaces black and isort with 10-100x better performance.
