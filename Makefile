# AI Doctor Agent - Makefile

.PHONY: help install run test clean docker-build docker-up docker-down logs

help:
	@echo "AI Doctor Agent - Available Commands"
	@echo ""
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run application (auto setup)"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make clean        - Clean temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make logs         - Show Docker logs"

install:
	@echo "Installing dependencies..."
	python -m venv .venv
	.venv/bin/pip install -r backend/requirements.txt

run:
	@echo "Starting AI Doctor Agent..."
	python run.py

test:
	@echo "Running tests..."
	pytest -v

test-cov:
	@echo "Running tests with coverage..."
	pytest --cov=backend --cov=data --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated: htmlcov/index.html"

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/ *.egg-info/
	@echo "Clean complete!"

docker-build:
	@echo "Building Docker image..."
	docker-compose build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo ""
	@echo "Services running:"
	@echo "  - Frontend: http://localhost:3000"
	@echo "  - Backend:  http://localhost:8000"
	@echo "  - API Docs: http://localhost:8000/docs"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

logs:
	docker-compose logs -f
