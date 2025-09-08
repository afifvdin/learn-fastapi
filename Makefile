format:
	@echo "Formatting..."
	uv run isort . --profile black
	uv run ruff format
	uv run ruff check --fix

dev: format
	@echo "Running app on localhost:8000..."
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000