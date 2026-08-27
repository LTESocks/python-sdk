.PHONY: sync-openapi generate generate-check format format-check lint typecheck test quality build

sync-openapi:
	uv run python scripts/sync_openapi.py $(SOURCE)

generate:
	uv run python scripts/generate.py

generate-check:
	uv run python scripts/check_generated.py

format:
	uv run ruff check --fix src tests scripts
	uv run ruff format src tests scripts

format-check:
	uv run ruff format --check src tests scripts

lint:
	uv run ruff check src tests scripts

typecheck:
	uv run mypy

test:
	uv run pytest

quality: format-check lint typecheck test

build:
	rm -rf build dist
	uv run python -m build
	uv run twine check dist/*
