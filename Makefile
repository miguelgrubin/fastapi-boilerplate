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

start:
	uv run python main.py http-server

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true

.PHONY: migrate
migrate:
	uv run alembic upgrade head

.PHONY: migrate-create
migrate-create:
	uv run alembic revision --autogenerate -m "$(m)"

.PHONY: migrate-downgrade
migrate-downgrade:
	uv run alembic downgrade -1

.PHONY: migrate-history
migrate-history:
	uv run alembic history --verbose

.PHONY: certs
certs:
	@mkdir -p docker/traefik/certs
	mkcert -cert-file docker/traefik/certs/local.crt \
	       -key-file docker/traefik/certs/local.key \
	       "*.localtest.me" "localtest.me"
	@echo "Certificates generated in docker/traefik/certs/"

.PHONY: docs
docs:
	uv run mkdocs build
	uv run mkdocs build -f mkdocs.es.yml

.PHONY: openapi
openapi:
	uv run python main.py export-openapi

.PHONY: docs-serve
docs-serve:
	uv run mkdocs serve

.PHONY: docs-serve-es
docs-serve-es:
	uv run mkdocs serve -f mkdocs.es.yml
