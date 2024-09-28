install:
	# Install Package Installer for Python
	pip install --upgrade pip && pip install -r requirements.txt

lint:
	# Lint Code with Ruff using pyproject.toml
	ruff check . --fix --config pyproject.toml

format:
	# Format Code with Ruff Formatter using pyproject.toml
	ruff format . --config pyproject.toml

test:
	# Test Code
	python -m pytest --cov=mylib test_logic.py

build:
	# Build Docker Image
	
run:
	# Run Docker Container
	
deploy:
	# Azure Deployment Setup with Docker
