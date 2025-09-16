# OpenMineral Platform Makefile

.PHONY: help install dev test lint format clean build deploy release

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)OpenMineral Platform - Make Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

dev: ## Start development environment
	@echo "$(BLUE)Starting development environment...$(NC)"
	docker compose --profile development up

dev-backend: ## Start backend only
	@echo "$(BLUE)Starting backend development server...$(NC)"
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend only
	@echo "$(BLUE)Starting frontend development server...$(NC)"
	cd frontend && npm run dev

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	cd backend && pytest tests/ -v --cov=backend/
	cd frontend && npm test
	@echo "$(GREEN)✅ All tests passed$(NC)"

test-backend: ## Run backend tests only
	@echo "$(BLUE)Running backend tests...$(NC)"
	cd backend && pytest tests/ -v --cov=backend/

test-frontend: ## Run frontend tests only
	@echo "$(BLUE)Running frontend tests...$(NC)"
	cd frontend && npm test

test-e2e: ## Run end-to-end tests
	@echo "$(BLUE)Running E2E tests...$(NC)"
	cd frontend && npm run test:e2e

lint: ## Run linting
	@echo "$(BLUE)Running linters...$(NC)"
	cd backend && flake8 . && mypy .
	cd frontend && npm run lint
	@echo "$(GREEN)✅ Linting completed$(NC)"

format: ## Format code
	@echo "$(BLUE)Formatting code...$(NC)"
	cd backend && black . && isort .
	cd frontend && npm run format
	@echo "$(GREEN)✅ Code formatted$(NC)"

clean: ## Clean build artifacts and caches
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	cd frontend && rm -rf node_modules/.cache build dist 2>/dev/null || true
	docker system prune -f
	@echo "$(GREEN)✅ Cleanup completed$(NC)"

build: ## Build all services
	@echo "$(BLUE)Building services...$(NC)"
	docker compose build
	@echo "$(GREEN)✅ Build completed$(NC)"

build-backend: ## Build backend Docker image
	@echo "$(BLUE)Building backend image...$(NC)"
	docker build -t openmineral/backend:latest backend/

build-frontend: ## Build frontend Docker image
	@echo "$(BLUE)Building frontend image...$(NC)"
	docker build -t openmineral/frontend:latest frontend/

docs: ## Build and serve documentation
	@echo "$(BLUE)Building documentation...$(NC)"
	cd docs && mkdocs serve

docs-build: ## Build documentation for production
	@echo "$(BLUE)Building documentation for production...$(NC)"
	cd docs && mkdocs build

deploy-local: ## Deploy to local Kubernetes
	@echo "$(BLUE)Deploying to local Kubernetes...$(NC)"
	kubectl apply -f kubernetes/manifests/
	@echo "$(GREEN)✅ Deployed to local cluster$(NC)"

deploy-staging: ## Deploy to staging environment
	@echo "$(BLUE)Deploying to staging...$(NC)"
	@echo "$(YELLOW)This would typically deploy to staging cluster$(NC)"
	# kubectl apply -f kubernetes/manifests/ --context staging

deploy-prod: ## Deploy to production environment
	@echo "$(BLUE)Deploying to production...$(NC)"
	@echo "$(YELLOW)This would typically deploy to production cluster$(NC)"
	# kubectl apply -f kubernetes/manifests/ --context production

release-patch: ## Create patch release
	@echo "$(BLUE)Creating patch release...$(NC)"
	python scripts/release.py --bump patch

release-minor: ## Create minor release
	@echo "$(BLUE)Creating minor release...$(NC)"
	python scripts/release.py --bump minor

release-major: ## Create major release
	@echo "$(BLUE)Creating major release...$(NC)"
	python scripts/release.py --bump major

release-dry-run: ## Show what release would do
	@echo "$(BLUE)Release dry run...$(NC)"
	python scripts/release.py --bump minor --dry-run

security-scan: ## Run security scans
	@echo "$(BLUE)Running security scans...$(NC)"
	cd backend && bandit -r . -f json -o security-report.json
	cd frontend && npm audit
	@echo "$(GREEN)✅ Security scan completed$(NC)"

performance-test: ## Run performance tests
	@echo "$(BLUE)Running performance tests...$(NC)"
	cd backend && python scripts/performance_test.py
	@echo "$(GREEN)✅ Performance tests completed$(NC)"

backup-db: ## Backup databases
	@echo "$(BLUE)Creating database backup...$(NC)"
	docker compose exec postgres pg_dump -U openmineral openmineral > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✅ Database backup created$(NC)"

monitoring: ## Setup monitoring stack
	@echo "$(BLUE)Setting up monitoring...$(NC)"
	kubectl apply -f monitoring/prometheus/
	kubectl apply -f monitoring/grafana/
	@echo "$(GREEN)✅ Monitoring stack deployed$(NC)"

ai-setup: ## Setup AI services and models
	@echo "$(BLUE)Setting up AI services...$(NC)"
	python scripts/setup_ai_models.py
	@echo "$(GREEN)✅ AI services configured$(NC)"

competitive-intel: ## Run competitive intelligence collection
	@echo "$(BLUE)Running competitive intelligence collection...$(NC)"
	python scripts/collect_competitive_intel.py
	@echo "$(GREEN)✅ Intelligence collection completed$(NC)"

init-project: ## Initialize new project setup
	@echo "$(BLUE)Initializing OpenMineral project...$(NC)"
	make install
	make build
	make dev
	@echo "$(GREEN)🎉 OpenMineral platform is ready!$(NC)"
	@echo "$(YELLOW)Access the platform at: http://localhost:3000$(NC)"
	@echo "$(YELLOW)API documentation at: http://localhost:8000/docs$(NC)"

# Version information
version: ## Show current version
	@python -c "import json; print('v' + json.load(open('frontend/package.json'))['version'])"

# Docker shortcuts
up: ## Start all services with Docker Compose
	docker compose up -d

down: ## Stop all services
	docker compose down

logs: ## Show logs from all services
	docker compose logs -f

restart: ## Restart all services
	docker compose restart

# Development shortcuts
install-dev: ## Install development dependencies
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	cd frontend && npm install
	pre-commit install

check: ## Run all checks (lint, type-check, test)
	make lint
	make test
	@echo "$(GREEN)✅ All checks passed$(NC)"