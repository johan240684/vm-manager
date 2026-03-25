.PHONY: help build up down logs clean test lint format install

help:
	@echo "VM Manager - Make Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make build        - Build Docker images"
	@echo "  make up           - Start all services"
	@echo "  make down         - Stop all services"
	@echo "  make logs         - View logs from all services"
	@echo "  make logs-backend - View backend logs"
	@echo "  make logs-frontend- View frontend logs"
	@echo "  make clean        - Remove containers and volumes"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Lint code"
	@echo "  make format       - Format code"
	@echo "  make install      - Install dependencies"
	@echo "  make backend-shell- Open backend container shell"
	@echo "  make frontend-shell-Open frontend container shell"

# Docker commands
build:
	@echo "Building Docker images..."
	docker-compose build

up:
	@echo "Starting services..."
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	@echo "Stopping services..."
	docker-compose down

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

# Development commands
install:
	@echo "Installing dependencies..."
	cd backend && pip install -r requirements.txt
	cd ../frontend && npm install

test:
	@echo "Running tests..."
	cd backend && pytest
	cd ../frontend && npm test

lint:
	@echo "Linting code..."
	cd backend && flake8 app || true
	cd ../frontend && npm run lint || true

format:
	@echo "Formatting code..."
	cd backend && black app || true
	cd frontend && prettier --write src || true

# Container commands
backend-shell:
	docker-compose exec backend /bin/bash

frontend-shell:
	docker-compose exec frontend /bin/sh

# Cleanup
clean:
	@echo "Cleaning up..."
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/node_modules frontend/dist
	@echo "Cleanup complete!"

# Database commands
db-migrate:
	docker-compose exec backend alembic upgrade head

db-reset:
	docker-compose exec backend rm vm_manager.db
	docker-compose restart backend

# Development server
dev-backend:
	cd backend && uvicorn app.main:app --reload

dev-frontend:
	cd frontend && npm start

# Production build
production-build: clean build
	@echo "Production build complete!"

# Push to registry (example)
push:
	docker tag vm-manager-backend:latest registry.example.com/vm-manager-backend:latest
	docker tag vm-manager-frontend:latest registry.example.com/vm-manager-frontend:latest
	docker push registry.example.com/vm-manager-backend:latest
	docker push registry.example.com/vm-manager-frontend:latest

# Init project
init: install build
	@echo "Project initialized!"
