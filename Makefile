# Makefile for managing the Cognitive SOAR application lifecycle.
# It automatically detects whether to use 'docker-compose' or 'docker compose'.

# --- Automatic Command Detection ---
# Check if the classic 'docker-compose' command is available.
# The '2>/dev/null' suppresses any "command not found" errors.
COMPOSE_CMD := $(shell command -v docker-compose 2>/dev/null)

# If the COMPOSE_CMD variable is empty, it means 'docker-compose' was not found.
# In that case, we fall back to the modern 'docker compose' syntax.
ifeq ($(COMPOSE_CMD),)
  COMPOSE_CMD := docker compose
endif
# --- End of Command Detection ---


# Phony targets are not actual files. This prevents conflicts.
.PHONY: all build up down logs clean status restart shell test

# The default command when running 'make' is 'make all', which runs 'make up'.
all: up

# Build or rebuild the service images defined in the compose file.
build:
	@echo "Building Cognitive SOAR Docker image(s) using '$(COMPOSE_CMD)'..."
	@$(COMPOSE_CMD) build

# Create and start containers. Includes '--build' to ensure images are up-to-date.
up:
	@echo "Starting Cognitive SOAR application using '$(COMPOSE_CMD)'..."
	@$(COMPOSE_CMD) up --build -d
	@echo ""
	@echo "Application is starting up in detached mode."
	@echo "View logs with: make logs"
	@echo "Check status with: make status"
	@echo "Access the app at: http://localhost:8501"

# Stop and remove containers, networks, and volumes created by 'up'.
down:
	@echo "Stopping Cognitive SOAR application using '$(COMPOSE_CMD)'..."
	@$(COMPOSE_CMD) down

# Follow the real-time logs from the application service.
logs:
	@echo "Following application logs... (Press Ctrl+C to exit)"
	@$(COMPOSE_CMD) logs -f

# Show the status of all containers.
status:
	@echo "Cognitive SOAR application status:"
	@$(COMPOSE_CMD) ps
	@echo ""
	@echo "Resource usage:"
	@$(COMPOSE_CMD) top

# Restart the application (stop and start).
restart: down up

# Access a shell inside the running container for debugging.
shell:
	@echo "Accessing shell inside Cognitive SOAR container..."
	@$(COMPOSE_CMD) exec mini-soar-app /bin/bash

# Run tests (placeholder for future test automation).
test:
	@echo "Running Cognitive SOAR tests..."
	@echo "Note: Manual testing procedures are documented in TESTING.md"
	@echo "To run tests manually:"
	@echo "1. Start the application: make up"
	@echo "2. Follow the test cases in TESTING.md"
	@echo "3. Check results in the web interface"

# A full cleanup: stops containers and removes generated files for a fresh start.
clean: down
	@echo "Cleaning up generated files and directories..."
	@rm -rf ./models
	@rm -rf ./data
	@echo "Cleanup complete. Run 'make up' to rebuild and retrain models."

# Show help information.
help:
	@echo "Cognitive SOAR - Available Commands:"
	@echo ""
	@echo "  make up      - Build and start the application"
	@echo "  make down    - Stop the application"
	@echo "  make logs    - View application logs"
	@echo "  make status  - Show container status and resource usage"
	@echo "  make restart - Restart the application"
	@echo "  make shell   - Access shell inside the container"
	@echo "  make test    - Show testing information"
	@echo "  make clean   - Clean up models and data (requires retraining)"
	@echo "  make build   - Rebuild Docker images"
	@echo "  make help    - Show this help message"
	@echo ""
	@echo "For detailed testing procedures, see TESTING.md"
	@echo "For installation help, see INSTALL.md"
