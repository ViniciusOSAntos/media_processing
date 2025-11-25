setup:
	@pip install -r requirements.txt

run:
	@uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload --workers 1

lint: ## Run lint
	@pylint app --disable=C0114

format: ## Run format
	@black . --line-length 79

test:
	python -m pytest tests/ --cov --cov-report term --cov-report xml:coverage.xml --junitxml=report.xml --cov-config=.coveragerc

docker_build:
	@docker-compose build

docker_start: docker_build
	@docker-compose up &

docker_stop:
	@docker-compose down

docker_clean:
	@docker-compose down -v --rmi all --remove-orphans
