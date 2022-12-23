.PHONY: run clean run

default: run logs

run:
	docker-compose --env-file .env up -d --build

stop:
	docker compose down

clean:
	docker compose down -v

logs:
	docker compose logs --follow
