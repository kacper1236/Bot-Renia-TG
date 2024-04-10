start: build run

build:
	cat .env > /dev/null && docker-compose build

run:
	docker-compose up -d

stop:
	docker-compose down

clear_db:
	rm -r ./data/

test:
	pytest tests/ -s