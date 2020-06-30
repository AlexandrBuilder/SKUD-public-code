start-prod:
	docker-compose -f docker-compose.prod.yml up -d --build

stop-prod:
	docker-compose -f docker-compose.prod.yml down

start-dev:
	docker-compose up --build

stop-dev:
	docker-compose down

update-db:
	docker-compose exec web flask db upgrade

drop-db:
	docker-compose exec web flask database drop

bash:
	docker-compose exec web bash




