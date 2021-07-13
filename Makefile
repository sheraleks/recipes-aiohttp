env:  ## create python env
	virtualenv -p ~/.pyenv/versions/3.7.4/bin/python env

install:  ## install requirements
	env/bin/pip install -r requirements.txt

test: ## run tests with pytest
	docker-compose up -d mongo
	env/bin/pytest --cov=app tests

run: ## run in local
	docker-compose up -d mongo
	PORT=8080 env/bin/watchmedo auto-restart -d app -p '*.py' -- env/bin/python -m app.main

run_in_docker: ## run in docker
	docker-compose build
	docker-compose up -d
