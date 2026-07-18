install:
	uv sync --system

dev-install:
	uv sync --group dev

dev: dev-install
	uv run flask --debug --app page_analyzer:app run

lint: dev-install
	uv run ruff check .

format: dev-install
	uv run ruff format .

test: dev-install
	uv run pytest

PORT ?= 8000

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh