PYTHONPATH = PYTHONPATH=./
RUN = $(PYTHONPATH) poetry run
TEST = $(RUN) pytest $(arg)
POETRY_RUN = poetry run
SERVICE_DIRS = .

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies
	poetry install --no-interaction --no-ansi --no-root --all-extras

.PHONY: format
format: ## Run linters in format mode
	$(POETRY_RUN) black $(SERVICE_DIRS)
	$(POETRY_RUN) ruff check --fix $(SERVICE_DIRS)
	$(POETRY_RUN) mypy $(SERVICE_DIRS)

.PHONY: lint
lint: ## Run linters in check mode
	$(POETRY_RUN) black --check $(SERVICE_DIRS)
	$(POETRY_RUN) ruff check $(SERVICE_DIRS)
	$(POETRY_RUN) mypy $(SERVICE_DIRS)

.PHONY: test
test: ## Runs pytest with coverage
	$(TEST) tests/
