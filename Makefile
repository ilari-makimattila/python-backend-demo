install:
	poetry install

dev:
	poetry run python -m demo_app http --dev

lint:
	poetry run ruff check .

typecheck:
	poetry run mypy --strict demo_app

check: lint typecheck

test:
	poetry run python -m pytest

