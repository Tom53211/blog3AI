.DEFAULT_GOAL := help

-include .env
export

IMAGE := $(GCP_REGION)-docker.pkg.dev/$(GOOGLE_CLOUD_PROJECT)/$(AR_REPO)/backend

.PHONY: help backend-sync backend-main backend-scrape docker-build docker-run \
        gcp-setup secrets-create docker-push job-deploy job-run scheduler-create

help: ## Show available targets
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

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

gcp-setup: ## Enable GCP APIs, create Artifact Registry repo, grant Secret Manager access to default Compute SA (run once)
	gcloud services enable \
		artifactregistry.googleapis.com \
		run.googleapis.com \
		secretmanager.googleapis.com \
		--project=$(GOOGLE_CLOUD_PROJECT)
	gcloud artifacts repositories describe $(AR_REPO) \
		--location=$(GCP_REGION) --project=$(GOOGLE_CLOUD_PROJECT) 2>/dev/null \
		|| gcloud artifacts repositories create $(AR_REPO) \
			--repository-format=docker \
			--location=$(GCP_REGION) \
			--project=$(GOOGLE_CLOUD_PROJECT)
	$(eval PROJECT_NUMBER := $(shell gcloud projects describe $(GOOGLE_CLOUD_PROJECT) --format='value(projectNumber)'))
	gcloud projects add-iam-policy-binding $(GOOGLE_CLOUD_PROJECT) \
		--member="serviceAccount:$(PROJECT_NUMBER)-compute@developer.gserviceaccount.com" \
		--role=roles/secretmanager.secretAccessor
	gcloud projects add-iam-policy-binding $(GOOGLE_CLOUD_PROJECT) \
		--member="serviceAccount:$(PROJECT_NUMBER)-compute@developer.gserviceaccount.com" \
		--role=roles/run.invoker
	gcloud services enable cloudscheduler.googleapis.com --project=$(GOOGLE_CLOUD_PROJECT)

secrets-create: ## Store FIRECRAWL_API_KEY and GOOGLE_API_KEY in Secret Manager (safe to re-run)
	@FIRECRAWL_KEY=$$(grep -oP 'FIRECRAWL_API_KEY=\K.*' .env); \
	 gcloud secrets create firecrawl-api-key --project=$(GOOGLE_CLOUD_PROJECT) 2>/dev/null || true; \
	 printf '%s' "$$FIRECRAWL_KEY" | gcloud secrets versions add firecrawl-api-key --data-file=- --project=$(GOOGLE_CLOUD_PROJECT)
	@GOOGLE_KEY=$$(grep -oP 'GOOGLE_API_KEY=\K.*' .env); \
	 gcloud secrets create google-api-key --project=$(GOOGLE_CLOUD_PROJECT) 2>/dev/null || true; \
	 printf '%s' "$$GOOGLE_KEY" | gcloud secrets versions add google-api-key --data-file=- --project=$(GOOGLE_CLOUD_PROJECT)

docker-push: docker-build ## Build and push the backend image to Artifact Registry
	gcloud auth configure-docker $(GCP_REGION)-docker.pkg.dev --quiet
	docker tag blog3ai-backend $(IMAGE):latest
	docker push $(IMAGE):latest

job-deploy: docker-push ## Build, push, and create-or-update the Cloud Run job
	gcloud run jobs deploy $(JOB_NAME) \
		--image=$(IMAGE):latest \
		--project=$(GOOGLE_CLOUD_PROJECT) \
		--region=$(GCP_REGION) \
		--set-env-vars=GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) \
		--set-secrets=FIRECRAWL_API_KEY=firecrawl-api-key:latest,GOOGLE_API_KEY=google-api-key:latest \
		--max-retries=1 \
		--task-timeout=15m

job-run: ## Manually trigger the Cloud Run job and wait for completion
	gcloud run jobs execute $(JOB_NAME) \
		--project=$(GOOGLE_CLOUD_PROJECT) \
		--region=$(GCP_REGION) \
		--wait

scheduler-create: ## Create Cloud Scheduler job to trigger scrape-blogs daily at 17:00 UTC (10 AM PDT)
	$(eval PROJECT_NUMBER := $(shell gcloud projects describe $(GOOGLE_CLOUD_PROJECT) --format='value(projectNumber)'))
	gcloud scheduler jobs create http scrape-blogs-schedule \
		--location=$(GCP_REGION) \
		--schedule="0 17 * * *" \
		--uri="https://$(GCP_REGION)-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$(GOOGLE_CLOUD_PROJECT)/jobs/$(JOB_NAME):run" \
		--http-method=POST \
		--oauth-service-account-email=$(PROJECT_NUMBER)-compute@developer.gserviceaccount.com \
		--project=$(GOOGLE_CLOUD_PROJECT)
