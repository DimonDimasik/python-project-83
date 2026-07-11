install:
	uv sync --group dev

dev:
	uv run flask --debug --app page_analyzer:app run

lint: install
	uv run ruff check.

format: install
	uv run ruff format .

test: dev-install
	uv run pytest

PORT ?= 8000

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app