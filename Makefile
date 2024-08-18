# コンテナ名
CONTAINER_NAME=api

# "api"が立ち上がっているか否かを判定
CHECK_CONTAINER=$(shell docker-compose ps -q $(CONTAINER_NAME) | xargs docker inspect -f '{{.State.Running}}' 2>/dev/null)

build:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build

run-dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

run-dev-d:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

stop:
	docker compose down

test:
	@if [ "$(CHECK_CONTAINER)" = "true" ]; then \
		echo "Container $(CONTAINER_NAME) is running. Running your command..."; \
		docker compose run --entrypoint "pytest" api; \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi

lint:
	@if [ "$(CHECK_CONTAINER)" = "true" ]; then \
		echo "Container $(CONTAINER_NAME) is running. Running your command..."; \
			docker compose run --entrypoint "flake8" api; \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi

format:
	@if [ "$(CHECK_CONTAINER)" = "true" ]; then \
		echo "Container $(CONTAINER_NAME) is running. Running your command..."; \
		docker compose run --entrypoint "black ." api; \
		docker compose run --entrypoint "flake8 " api; \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi
