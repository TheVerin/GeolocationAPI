build:
	docker-compose build

run:
	docker-compose up -d

migrate:
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate

premium:
	docker-compose exec web python manage.py create_premium_group

test:
	docker-compose exec web python manage.py test && flake8

stop:
	docker-compose down -v

bash:
	docker-compose exec web bash

setup: build run migrate premium

run-tests: setup test stop
