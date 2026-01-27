DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
STORAGES_CONTAINER = postgres
MESSAGING_FILE = docker_compose/messaging.yaml
MESSAGING_CONTAINER = rabbitmq
MAIL_FILE = docker_compose/mail.yaml
MAIL_CONTAINER = maildev
LOGS = docker logs
ENV = --env-file .env
EXEC = docker exec -it
EXEC_NO_TTY = docker exec
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = main-app

# Application ==============================================================

.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${MESSAGING_FILE} -f ${MAIL_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${STORAGES_FILE} -f ${MESSAGING_FILE} -f ${MAIL_FILE} -f ${APP_FILE} ${ENV} down

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

# Messaging ================================================================

.PHONY: messaging
messaging:
	${DC} -f ${MESSAGING_FILE} ${ENV} up --build -d

.PHONY: messaging-down
messaging-down:
	${DC} -f ${MESSAGING_FILE} ${ENV} down

.PHONY: messaging-logs
messaging-logs:
	${LOGS} ${MESSAGING_CONTAINER} -f

# Mail ====================================================================

.PHONY: mail
mail:
	${DC} -f ${MAIL_FILE} ${ENV} up --build -d

.PHONY: mail-down
mail-down:
	${DC} -f ${MAIL_FILE} ${ENV} down

.PHONY: mail-logs
mail-logs:
	${LOGS} ${MAIL_CONTAINER} -f

# Precommit ===============================================================

.PHONY: precommit 
precommit:
	pre-commit run --all-files

# Tests ===================================================================

.PHONY: test 
test:
	${EXEC} ${APP_CONTAINER} pytest

.PHONY: test-domain
test-domain:
	${EXEC} ${APP_CONTAINER} pytest tests/domain

.PHONY: test-logic
test-logic:
	${EXEC} ${APP_CONTAINER} pytest tests/application

.PHONY: test-e2e
test-e2e:
	${EXEC} ${APP_CONTAINER} pytest tests/presentation
