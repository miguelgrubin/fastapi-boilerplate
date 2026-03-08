.PHONY: install-uv
install-uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

.PHONY: install
install:
	uv sync --all-extras

.PHONY: typecheck
typecheck:
	uv run ty check src

.PHONY: format-check
format-check:
	uv run ruff format --check .
	uv run ruff check --select I .

.PHONY: format
format:
	uv run ruff check --select I --fix .
	uv run ruff format .

.PHONY: test
test:
	uv run pytest tests

.PHONY: coverage
coverage:
	uv run coverage run -m pytest tests
	uv run coverage report

.PHONY: coverage-html
coverage-html:
	uv run coverage run -m pytest tests
	uv run coverage html
	@echo "HTML report generated in htmlcov/index.html"

.PHONY: lint
lint:
	PYTHONPATH=./src uv run pylint ./src

.PHONY: start
start:
	uv run python main.py http-server

.PHONY: start-debug
start-debug:
	DEBUG=true uv run python main.py http-server

# Docker Compose commands
.PHONY: docker-services-up
docker-services-up:
	docker compose up -d
	@echo "✅ Services started: PostgreSQL, Redis, Authelia, Traefik"
	@echo "   PostgreSQL: localhost:15432"
	@echo "   Redis: localhost:6379"
	@echo "   Traefik Dashboard: http://localhost:8080"
	@echo "   Authelia: https://auth.localtest.me"

.PHONY: docker-services-down
docker-services-down:
	docker compose down
	@echo "✅ Services stopped"

.PHONY: docker-services-logs
docker-services-logs:
	docker compose logs -f

.PHONY: docker-services-ps
docker-services-ps:
	docker compose ps

.PHONY: docker-services-clean
docker-services-clean:
	docker compose down -v
	@echo "✅ Services and volumes cleaned"

.PHONY: docker-dev-up
docker-dev-up:
	docker compose -f compose.dev.yml up -d
	@echo "✅ Full stack started (services + app)"
	@echo "   App: http://localhost:8000"
	@echo "   App (with proxy): https://blog.localtest.me"
	@echo "   Debugger: localhost:5678"

.PHONY: docker-dev-down
docker-dev-down:
	docker compose -f compose.dev.yml down
	@echo "✅ Full stack stopped"

.PHONY: docker-dev-logs
docker-dev-logs:
	docker compose -f compose.dev.yml logs -f app

.PHONY: docker-dev-logs-all
docker-dev-logs-all:
	docker compose -f compose.dev.yml logs -f

.PHONY: docker-dev-ps
docker-dev-ps:
	docker compose -f compose.dev.yml ps

.PHONY: docker-dev-clean
docker-dev-clean:
	docker compose -f compose.dev.yml down -v
	@echo "✅ Full stack and volumes cleaned"

.PHONY: docker-dev-rebuild
docker-dev-rebuild:
	docker compose -f compose.dev.yml up -d --build
	@echo "✅ Full stack rebuilt and started"

.PHONY: docker-db-connect
docker-db-connect:
	docker compose exec postgres psql -U fastapi -d fastapi_db

.PHONY: docker-redis-connect
docker-redis-connect:
	docker compose exec redis redis-cli

.PHONY: docker-app-shell
docker-app-shell:
	docker compose -f compose.dev.yml exec app /bin/sh

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

.PHONY: help
help:
	@echo "FastAPI Boilerplate - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install              Install dependencies"
	@echo "  make typecheck            Run type checker (ty)"
	@echo "  make format               Format code with ruff"
	@echo "  make format-check         Check formatting"
	@echo "  make lint                 Run pylint"
	@echo "  make test                 Run tests"
	@echo "  make coverage             Run tests with coverage"
	@echo "  make coverage-html        Generate HTML coverage report"
	@echo ""
	@echo "Local Development:"
	@echo "  make start                Start app locally"
	@echo "  make start-debug          Start app with debugger enabled"
	@echo ""
	@echo "Docker Services (PostgreSQL, Redis, Authelia, Traefik):"
	@echo "  make docker-services-up   Start services"
	@echo "  make docker-services-down Stop services"
	@echo "  make docker-services-ps   List running services"
	@echo "  make docker-services-logs View service logs"
	@echo "  make docker-services-clean Stop and remove volumes"
	@echo ""
	@echo "Docker Full Stack (services + app):"
	@echo "  make docker-dev-up        Start everything"
	@echo "  make docker-dev-down      Stop everything"
	@echo "  make docker-dev-ps        List containers"
	@echo "  make docker-dev-logs      View app logs"
	@echo "  make docker-dev-logs-all  View all logs"
	@echo "  make docker-dev-rebuild   Rebuild and start"
	@echo "  make docker-dev-clean     Stop and remove volumes"
	@echo ""
	@echo "Database Access:"
	@echo "  make docker-db-connect    Connect to PostgreSQL"
	@echo "  make docker-redis-connect Connect to Redis"
	@echo "  make docker-app-shell     Shell into app container"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean                Remove cache files"
	@echo "  make help                 Show this help"