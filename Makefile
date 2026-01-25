DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
STORAGES_CONTAINER = postgres
LOGS = docker logs
ENV = --env-file .env
EXEC = docker exec -it
EXEC_NO_TTY = docker exec
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = main-app

# Application ==============================================================

.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} ${ENV} down

.PHONY: app-up
app-up:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} ${ENV} up --build -d main-app

# Storages ================================================================

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} ${ENV} down

.PHONY: storages-logs
storages-logs:
	${LOGS} ${STORAGES_CONTAINER} -f

# Precommit ===============================================================

.PHONY: precommit 
precommit:
	pre-commit run --all-files

# Tests ===================================================================

.PHONY: test 
test:
	${EXEC} ${APP_CONTAINER} pytest
