.DEFAULT_GOAL := help

.PHONY: help backend-sync backend-run docker-build docker-run docker-run-test

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

backend-sync: ## Create/update backend venv and install dependencies with uv sync
	uv sync --directory src/backend

backend-main: ## Run the backend main script
	uv run --directory src/backend --env-file ../../.env python main.py
