install:
	poetry install

run-db:
	docker compose up -d database

dev: run-db
	poetry run python -m demo_app http --dev

dev-docker:
	docker compose up -d database
	docker compose run --rm app migrate
	docker compose run --rm app

lint:
	poetry run ruff check .

typecheck:
	poetry run mypy --strict demo_app

check: lint typecheck

test: run-db
	poetry run python -m pytest

