
all:
	@trap 'kill $$(jobs -p)' EXIT; \
	bun --cwd frontend dev & \
	cd backend && uv run main.py & \
	wait

dev:
	cd backend && uv run main.py


test:
	cd backend && uv run pytest -v tests


fe:
	bun --cwd frontend dev

build: fe
	bun --cwd frontend build
	@echo "Build complete"


