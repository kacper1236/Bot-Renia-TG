start: build run

build:
	cat .env &> /dev/null && docker-compose build

run:
	docker-compose up -d

clear_db:
	rm -r ./data/