.PHONY: test
test:
	uv run pytest -vv

.PHONY: typecheck
typecheck:
	uv run mypy

.PHONY: pre-commit-setup
pre-commit-setup:
	uv run pre-commit install
	uv run pre-commit run --all-files
