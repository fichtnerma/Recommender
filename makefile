.PHONY: run clean run

default: run logs

run:
	cd bibrec && docker compose up -d --build

stop:
	cd bibrec && docker compose down

clean:
	cd bibrec && docker compose down -v

logs:
	cd bibrec && docker compose logs --follow
