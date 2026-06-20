.PHONY: up down build migrate

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

migrate:
	docker-compose exec backend alembic upgrade head