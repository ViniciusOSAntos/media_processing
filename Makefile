setup:
	@pip install -r requirements.txt

run:
	@uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --workers 1

lint: ## Run lint
	@pylint app --disable=C0114

format: ## Run format
	@black . --line-length 79
