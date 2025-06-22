
lint: 
	black .
	isort .
	ruff check . --fix 
	mypy . --pretty --ignore-missing-imports