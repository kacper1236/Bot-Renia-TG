start: build run

build:
	cat .env &> /dev/null && docker compose build

run:
	docker compose up -d

stop:
	docker compose down -v

test:
	pytest tests/ -s
