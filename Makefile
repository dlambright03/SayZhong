.PHONY: help install install-dev test test-cov lint format clean build docs serve-docs

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install package in development mode"
	@echo "  install-dev  - Install package with development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage report"
	@echo "  lint         - Run all linting tools"
	@echo "  format       - Format code with black and isort"
	@echo "  clean        - Remove build artifacts and cache files"
	@echo "  build        - Build package for distribution"
	@echo "  docs         - Build documentation"
	@echo "  serve-docs   - Serve documentation locally"
	@echo "  pre-commit   - Install pre-commit hooks"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

# Testing
test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ --cov=src/sayzhong --cov-report=term-missing --cov-report=html

# Code quality
lint:
	python -m flake8 src/ tests/
	python -m mypy src/
	python -m black --check src/ tests/
	python -m isort --check-only src/ tests/

format:
	python -m black src/ tests/
	python -m isort src/ tests/

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	python -m build

# Documentation
docs:
	mkdocs build

serve-docs:
	mkdocs serve

# Development setup
pre-commit:
	pre-commit install