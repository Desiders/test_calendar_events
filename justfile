package_dir := "src"

# Show help message
help:
    just -l

# Install package with dependencies
install:
	pip install -r requirements.txt

# Run app in docker container
up:
	docker compose --profile api up --build

# Stop docker containers
down:
	docker compose --profile api down

# Build docker image
build:
	docker compose build

# Run migration for postgres database
migrate:
	docker compose --profile migration up --build

# Compile tailwind css
tailwindcss:
	npx tailwindcss -i ./unpublic/css/tailwind.css -o ./static/css/styles.css