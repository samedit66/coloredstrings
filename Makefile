.PHONY: check lint format-check test typecheck pre-commit-setup

check: lint format-check typecheck test

lint:
	uv run --frozen ruff check .

format-check:
	uv run --frozen ruff format --check .

test:
	uv run --frozen pytest -q

typecheck:
	uv run --frozen mypy

pre-commit-setup:
	uv run --frozen pre-commit install
	uv run --frozen pre-commit run --all-files
