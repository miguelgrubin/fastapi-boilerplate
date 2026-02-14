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
