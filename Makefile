.PHONY: sync
sync:
	uv sync --all-extras --all-packages

.PHONY: docker-buildx
docker-buildx:
	docker buildx build --no-cache --pull --platform linux/amd64 -f Dockerfile -t pyquiz .

.PHONY: docker-run
docker-run:
	docker run --rm -it pyquiz

.PHONY: tests
tests:
	uv run pytest -v --color=yes --tb=short

.PHONY: coverage
coverage:
	uv run pytest -v --color=yes --tb=short --cov=apps --cov-report=term-missing --cov-report=html --cov-report=xml