.PHONY: help install dev run clean lint format test check

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies with uv
	uv sync

dev: ## Install all dependencies including dev tools
	uv sync --all-extras

run: ## Run the FastMCP server
	uv run python main.py

clean: ## Clean up caches and temporary files
	rm -rf __pycache__ .pytest_cache .coverage htmlcov/ .uv_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

lint: ## Run linting with ruff
	uv run ruff check .

format: ## Format code with black and isort
	uv run black .
	uv run isort .

type-check: ## Run type checking with mypy
	uv run mypy .

test: ## Run tests with pytest
	uv run pytest

check: lint type-check ## Run all code quality checks

setup: ## Quick setup for new users
	./setup.sh
