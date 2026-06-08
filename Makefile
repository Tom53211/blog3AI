BACKEND_DIR := src/backend

.DEFAULT_GOAL := help

.PHONY: help setup backend-sync

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

backend-sync: ## Create/update backend venv and install dependencies with uv sync
	@command -v uv >/dev/null 2>&1 || { echo "error: uv is not installed (https://docs.astral.sh/uv/)"; exit 1; }
	uv sync --directory $(BACKEND_DIR)
