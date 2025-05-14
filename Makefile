.DEFAULT_GOAL := default

.PHONY: default

default: check format lint

check:
	uv run ruff check --fix scripts/ src/

format:
	uv run ruff format scripts/ src/

lint:
	basedpyright scripts/ src/
