dev:
	uv run main.py

test:
	uv run pytest -v tests


fe:
	bun --cwd frontend build
	
