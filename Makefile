.DEFAULT_GOAL := help

.PHONY: help backend-sync backend-run docker-build docker-run

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

backend-sync: ## Create/update backend venv and install dependencies with uv sync
	uv sync --directory src/backend

backend-main: ## Run the backend main script
	uv run --directory src/backend --env-file ../../.env python main.py

backend-scrape: ## Run the backend scrape script
	uv run --directory src/backend --env-file ../../.env python scrape_blogs.py

docker-build: ## Build the backend Docker image
	docker build -t blog3ai-backend src/backend

docker-run: ## Run the backend Docker image (loads .env, mounts host ADC)
	docker run --rm --env-file .env \
		-v $(HOME)/.config/gcloud:/root/.config/gcloud:ro \
		-e GOOGLE_APPLICATION_CREDENTIALS=/root/.config/gcloud/application_default_credentials.json \
		blog3ai-backend
