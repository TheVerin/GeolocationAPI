# Dev stage

# Build docker image on base settings
build-dev:
	docker-compose -f docker-compose.yml build

# Run app on base settings
run-dev:
	docker-compose -f docker-compose.yml up -d

# Run app on base settings with migrations and creating premium group
setup-dev:
	docker-compose -f docker-compose.yml build
	docker-compose -f docker-compose.yml up -d
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py create_premium_group

# Set up containers on base settings then test and if tests pass stop and remove all containers.
test-dev:
	docker-compose -f docker-compose.yml build
	docker-compose -f docker-compose.yml up -d
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py create_premium_group
	docker-compose exec web coverage run --source='.' manage.py test && flake8
	docker-compose exec web coverage report -m
	docker-compose down -v


# Production stage

# Build docker image on production settings
build-prod:
	docker-compose -f docker-compose.prod.yml build

# Run app on production settings
run-prod:
	docker-compose -f docker-compose.prod.yml up -d

# Run app on base settings with collect static files, migrations and creating premium group
setup-prod:
	docker-compose -f docker-compose.prod.yml build
	docker-compose -f docker-compose.prod.yml up -d
	docker-compose exec web python manage.py collectstatic --noinput
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py create_premium_group

# Set up containers on production settings then test and if tests pass stop and remove all
# containers.
test-prod:
	docker-compose -f docker-compose.prod.yml build
	docker-compose -f docker-compose.prod.yml up -d
	docker-compose exec web python manage.py collectstatic --noinput
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py create_premium_group
	docker-compose exec web coverage run --source='.' manage.py test && flake8
	docker-compose exec web coverage report -m
	docker-compose down -v
