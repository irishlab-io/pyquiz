.PHONY: sync
sync:
	uv sync --all-extras --all-packages

.PHONY: docker-buildx
docker-buildx:
	docker buildx build --no-cache --pull --platform linux/amd64,linux/arm64 -f Dockerfile -t pyquiz .

.PHONY: docker-run
docker-run:
	docker run --rm -it pyquiz

.PHONY: tests
tests:
	uv run pytest -v --color=yes --tb=short

.PHONY: coverage
coverage:
	uv run pytest -v --color=yes --tb=short --cov=apps --cov-report=term-missing --cov-report=html --cov-report=xml

.PHONY: move-pre-commit
SRC_FILE0 ?= docs/prep/
SRC_DIR ?= $(STEP)
SRC_FILE1 ?= not.pre-commit-config.yaml

move-pre-commit:
	@SRC="$(SRC_FILE0)$(SRC_DIR)/$(SRC_FILE1)"; \
	DST=.pre-commit-config.yaml; \
	cp "$$SRC" "$$DST"; \
