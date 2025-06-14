# Multi-Agent System Makefile

.PHONY: help setup install run-api run-ui run-both test clean lint format

# Default target
help:
	@echo "🤖 Multi-Agent System Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup      - Full setup (install deps + models)"
	@echo "  make install    - Install Python dependencies only"
	@echo "  make run-web-install - Install web dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run-api    - Start API server only"
	@echo "  make run-ui     - Start Streamlit UI only"
	@echo "  make run-web    - Start Next.js web app"
	@echo "  make run-both   - Start both API and Web"
	@echo "  make run        - Alias for run-both"
	@echo ""
	@echo "Development:"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean temporary files"
	@echo ""
	@echo "Ollama:"
	@echo "  make ollama-start    - Start Ollama service"
	@echo "  make ollama-status   - Check Ollama status"
	@echo "  make ollama-models   - List available models"

# Setup and installation
setup:
	@echo "🚀 Running full setup..."
	python -m scripts.setup

install:
	@echo "📦 Installing dependencies..."
	pip install -e .

# Running services
run-api:
	@echo "🌐 Starting API server..."
	python -m scripts.run api

run-ui:
	@echo "🎨 Starting Streamlit UI..."
	python -m scripts.run ui

run-web:
	@echo "🌐 Starting Next.js web app..."
	cd ui/web && npm run dev

run-web-install:
	@echo "📦 Installing web dependencies..."
	cd ui/web && npm install

run-both run:
	@echo "🚀 Starting both API and Web services..."
	python -m scripts.run api & cd ui/web && npm run dev

# Development
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

lint:
	@echo "🔍 Running linter..."
	python -m ruff check .
	python -m mypy agents/ api/ ui/ utils/

format:
	@echo "✨ Formatting code..."
	python -m ruff format .
	python -m ruff check --fix .

clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Ollama management
ollama-start:
	@echo "🤖 Starting Ollama..."
	ollama serve

ollama-status:
	@echo "📊 Checking Ollama status..."
	ollama list

ollama-models:
	@echo "📋 Available models:"
	ollama list

# Quick development shortcuts
dev: install run-both

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	@echo "Note: Implement your deployment strategy here"

# Docker support (if needed)
docker-build:
	docker build -t multi-agent-system .

docker-run:
	docker run -p 8000:8000 -p 8501:8501 multi-agent-system 