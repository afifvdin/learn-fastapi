prod-docker-up:
	@echo "(prod) Up docker..."
	docker compose -f docker-compose.prod.yaml up -d

prod-docker-down:
	@echo "(prod) Down docker..."
	docker compose -f docker-compose.prod.yaml down

prod-docker-build:
	@echo "(prod) Running docker build..."
	docker compose -f docker-compose.prod.yaml build

dev-docker-up:
	@echo "(dev) Up docker..."
	docker compose -f docker-compose.dev.yaml up -d

dev-docker-down:
	@echo "(dev) Down docker..."
	docker compose -f docker-compose.dev.yaml down

dev-db-init:
	@echo "Running database initialization..."
	uv run alembic init alembic

dev-db-generate:
	@echo "Running migration ($m)..."
	uv run alembic revision --autogenerate -m "$m"

dev-db-peek:
	@echo "Peeking head migration..."
	uv run alembic upgrade head --sql

dev-db-up:
	@echo "Upgrade migration..."
	uv run alembic upgrade head

dev-db-down:
	@echo "Downgrade migration..."
	uv run alembic upgrade head

format:
	@echo "Formatting..."
	uv run ruff format .
	uv run ruff check . --fix

dev: format
	@echo "Running app on localhost:8000..."
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000