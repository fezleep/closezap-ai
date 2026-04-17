.PHONY: help install run test clean migrate docker-up docker-down

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

run: ## Run the development server
	python run.py

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=app --cov-report=html

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -f .coverage
	rm -rf htmlcov/

migrate: ## Run database migrations
	alembic upgrade head

migration: ## Create a new migration
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-build: ## Build Docker image
	docker-compose build

lint: ## Run code linting
	flake8 app/ tests/

format: ## Format code
	black app/ tests/