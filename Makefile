.PHONY: help up down logs restart health

help:
	@echo "Comandos disponibles:"
	@echo "  make up      -> levanta backend + frontend con Docker"
	@echo "  make down    -> para y elimina contenedores"
	@echo "  make logs    -> muestra logs en tiempo real"
	@echo "  make restart -> reinicia servicios"
	@echo "  make health  -> prueba que el backend responde"

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

restart: down up

health:
	curl -s http://localhost:8000/health
