# Variables
DOCKER_COMPOSE = docker-compose -f
DOCKER_COMPOSE_FILE = docker-compose.yml

# Commands
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@grep -E '^[a-zA-Z0-9_\-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

.PHONY: up
up:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) up

.PHONY: down
down:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) down

.PHONY: logs
logs:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) logs -f

.PHONY: shell
shell:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) exec fastapi sh

.PHONY: lint
lint:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) exec fastapi flake8 .

.PHONY: test
test:
	$(DOCKER_COMPOSE) $(DOCKER_COMPOSE_FILE) exec fastapi pytest

.PHONY: build
build:
	docker build -t my_fastapi_app .

.PHONY: run-new
run-new: build up
