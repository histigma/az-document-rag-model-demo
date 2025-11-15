BACKEND_DIR = backend/src
BACKEND_APP = main:app 
BACKEND_PORT = 8000

FRONTEND_DIR = frontend/src
FRONTEND_APP = app.py 
FRONTEND_PORT = 8501

PID_FILE = .server_pids

# =========================================================

.PHONY: all up down clean dockercompose_up backend_up frontend_up

all: up

up: dockercompose_up backend_up frontend_up

backend_up:
	@echo "Starting FastAPI Backend on port $(BACKEND_PORT)..."
	cd $(BACKEND_DIR) && uvicorn $(BACKEND_APP) --host 0.0.0.0 --port $(BACKEND_PORT) --log-level info &
	echo $$! > $(PID_FILE)

frontend_up:
	@echo "Starting Streamlit Frontend on port $(FRONTEND_PORT)..."
	cd $(FRONTEND_DIR) && streamlit run $(FRONTEND_APP) --server.port $(FRONTEND_PORT)

dockercompose_up:
	@echo "Starting docker compose..."
	docker compose up -d

down:
	@echo "Stopping services..."
	@echo "Stopping Docker Compose containers..."
	docker compose down
	if [ -f $(PID_FILE) ]; then \
		kill -9 `cat $(PID_FILE)`; \
		rm $(PID_FILE); \
		echo "FastAPI Backend stopped."; \
	else \
		echo "No running server PIDs found in $(PID_FILE)."; \
	fi
	@echo "All services stopped."

clean: down
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
