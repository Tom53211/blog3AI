BACKEND_DIR := src/backend
IMAGE_NAME := blog3ai-scraper
IMAGE_TAG ?= latest
DOCKER_IMAGE := $(IMAGE_NAME):$(IMAGE_TAG)
GCP_ADC := $(HOME)/.config/gcloud/application_default_credentials.json
HOST_CA_BUNDLE := $(shell python3 -c "import ssl; print(ssl.get_default_verify_paths().cafile or '')" 2>/dev/null)
DOCKER_CACHE_DIR := .docker
DOCKER_CA_BUNDLE := $(DOCKER_CACHE_DIR)/ca-bundle.pem

.DEFAULT_GOAL := help

.PHONY: help backend-sync backend-run docker-build docker-run docker-run-test

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

backend-sync: ## Create/update backend venv and install dependencies with uv sync
	@command -v uv >/dev/null 2>&1 || { echo "error: uv is not installed (https://docs.astral.sh/uv/)"; exit 1; }
	uv sync --directory $(BACKEND_DIR)

backend-run: backend-sync ## Run the backend
	cd $(BACKEND_DIR) && uv run python main.py

docker-build: ## Build the scraper Docker image
	docker build -t $(DOCKER_IMAGE) .

docker-run: docker-build ## Run the scraper in Docker (loads .env, gcloud ADC, and host CA bundle if present)
	@set -a; [ -f .env ] && . ./.env; set +a; \
	GCP_MOUNT=; \
	CERT_MOUNT=; \
	if [ -f "$(GCP_ADC)" ]; then \
		GCP_MOUNT="-v $(GCP_ADC):/secrets/gcp.json:ro -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp.json"; \
	fi; \
	CA_BUNDLE="$${SSL_CERT_FILE:-$${REQUESTS_CA_BUNDLE:-$(HOST_CA_BUNDLE)}}"; \
	if [ -n "$$CA_BUNDLE" ] && [ -f "$$CA_BUNDLE" ]; then \
		mkdir -p $(DOCKER_CACHE_DIR); \
		cp "$$CA_BUNDLE" "$(DOCKER_CA_BUNDLE)"; \
		CERT_MOUNT="-v $(DOCKER_CA_BUNDLE):/etc/ssl/certs/host-ca-bundle.pem:ro -e SSL_CERT_FILE=/etc/ssl/certs/host-ca-bundle.pem -e REQUESTS_CA_BUNDLE=/etc/ssl/certs/host-ca-bundle.pem"; \
	fi; \
	docker run --rm \
		-e GOOGLE_PROJECT \
		-e GOOGLE_REGION \
		-e FIRECRAWL_API_KEY \
		$$GCP_MOUNT \
		$$CERT_MOUNT \
		$(DOCKER_IMAGE)
