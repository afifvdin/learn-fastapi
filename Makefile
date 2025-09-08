db-generate:
	@echo "Running migration ($1)"
	uv run alembic revision --autogenerate -m "$1"

db-peek:
	@echo "Peeking head migration"
	uv run alembic upgrade head --sql

db-up:
	@echo "Upgrade migration"
	uv run alembic upgrade head

db-down:
	@echo "Downgrade migration"
	uv run alembic upgrade head

format:
	@echo "Formatting..."
	uv run ruff format
	uv run ruff check --fix

format-old:
	@echo "Formatting..."
	uv run isort . --profile black
	uv run black .

dev: format
	@echo "Running app on localhost:8000..."
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000