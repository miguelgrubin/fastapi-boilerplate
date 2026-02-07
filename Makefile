.PHONY: install-uv
install-uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

.PHONY: install
install:
	uv sync --all-extras

.PHONY: typecheck
typecheck:
	uv run mypy src

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
	PYTHONPATH=./src uv run uvicorn main:app --reload
