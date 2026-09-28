.PHONY: test generate up down

test:
	bash scripts/run_tests.sh

generate:
	python generator/generate_events.py --users 5000 --days 14 --out data/events.jsonl

up:
	docker compose up -d

down:
	docker compose down -v
