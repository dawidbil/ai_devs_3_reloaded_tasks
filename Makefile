.DEFAULT_GOAL := default

.PHONY: default

default: check format lint

check:
	uv run ruff check --fix scripts/

format:
	uv run ruff format scripts/

lint:
	basedpyright scripts/
