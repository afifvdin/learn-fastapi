init-db:
	@echo "Running database initialization..."
	uv run alembic run init alembic

db-generate:
	@echo "Running migration ($m)..."
	uv run alembic revision --autogenerate -m "$m"

db-peek:
	@echo "Peeking head migration..."
	uv run alembic upgrade head --sql

db-up:
	@echo "Upgrade migration..."
	uv run alembic upgrade head

db-down:
	@echo "Downgrade migration..."
	uv run alembic upgrade head

format:
	@echo "Formatting..."
	uv run ruff format
	uv run ruff check --fix

dev: format
	@echo "Running app on localhost:8000..."
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000