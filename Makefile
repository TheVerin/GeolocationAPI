build-dev:
	docker-compose -f docker-compose.yml build

run-dev:
	docker-compose -f docker-compose.yml up -d

build-prod:
	docker-compose -f docker-compose.prod.yml build

run-prod:
	docker-compose -f docker-compose.prod.yml up -d

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


setup-dev: build-dev run-dev migrate premium

run-tests-dev: setup-dev test stop


setup-prod: build-prod run-prod migrate premium

run-tests-prod: setup-prod test stop
