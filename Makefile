# コンテナ名
CONTAINER_NAME=api

# "api"が立ち上がっているか否かを判定
CHECK_CONTAINER=$(shell docker-compose ps -q $(CONTAINER_NAME) | xargs docker inspect -f '{{.State.Running}}' 2>/dev/null)

.PHONY: build
build: ## ビルド
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build

.PHONY: build-no-cache
build-no-cache: ## ビルド
	docker compose -f docker-compose.yml -f docker-compose.dev.yml build --no-cache

.PHONY: run-dev
run-dev: ## コンテナ起動
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

.PHONY: run-dev-d
run-dev-d: ## コンテナ起動（デタッチ）
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

.PHONY: stop
stop: ## コンテナ停止
	docker compose down

.PHONY: create-table
create-table: ## テーブル作成
	@if [ "$(CHECK_CONTAINER)" = "true" ]; then \
		echo "Container $(CONTAINER_NAME) is running. Running your command..."; \
		docker compose exec $(CONTAINER_NAME) python migrate_db.py; \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi

.PHONY: migrate
migrate: ## マイグレーション実行
	@if [ "$(CHECK_CONTAINER)" = "true" ]; then \
		echo "Container $(CONTAINER_NAME) is running. Running your command..."; \
		docker compose exec $(CONTAINER_NAME) alembic upgrade head; \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi

.PHONY: test
test: ## テスト
	@if [ "$(CHECK_CONTAINER)" = "true" ]; then \
		echo "Container $(CONTAINER_NAME) is running. Running your command..."; \
		docker compose exec $(CONTAINER_NAME) pytest --asyncio-mode=auto; \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi

.PHONY: lint
lint: ## リント
	@if [ "$(CHECK_CONTAINER)" = "true" ]; then \
		echo "Container $(CONTAINER_NAME) is running. Running your command..."; \
		docker compose exec $(CONTAINER_NAME) flake8; \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi

.PHONY: format
format: ## フォーマット
	@if [ "$(CHECK_CONTAINER)" = "true" ]; then \
		echo "Container $(CONTAINER_NAME) is running. Running your command..."; \
		docker compose exec $(CONTAINER_NAME) black .; \
		docker compose exec $(CONTAINER_NAME) isort .; \
		docker compose exec $(CONTAINER_NAME) flake8; \
	else \
		echo "Container $(CONTAINER_NAME) is not running."; \
	fi

.PHONY: pre-commit
pre-commit: format lint test
