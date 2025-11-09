.PHONY: install dev test lint format clean run docker-build docker-up docker-down docker-dev

# Install dependencies
install:
	uv sync

# Install development dependencies
dev:
	uv sync --extra dev
	uv run pre-commit install

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term

# Lint code
lint:
	uv run ruff check src tests
	uv run mypy src

# Format code
format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

# Clean cache and build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Run development server
run:
	uv run python main.py

# Run with auto-reload
dev-server:
	uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Docker commands
docker-build:
	docker build -t multi-agent-rag-system .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

docker-logs:
	docker-compose logs -f app

docker-clean:
	docker-compose down -v
	docker system prune -f