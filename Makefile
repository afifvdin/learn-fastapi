docker-build:
	@echo "Running docker build..."
	docker build -t afifvdin/learn-fastapi .

docker-build-platform:
	@echo "Running docker build (platform)..."
	docker build --platform linux/amd64 -t afifvdin/learn-fastapi .

docker run:
	@echo "Running through docker..."
	docker run -p 8000:8000 --name myapp -d afifvdin/learn-fastapi

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