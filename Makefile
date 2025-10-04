.PHONY: test
test:
	uv run pytest -vv

.PHONY: typecheck
typecheck:
	uv run mypy src
