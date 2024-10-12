DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker-compose.yml
APP_CONTAINER = web

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-rebuild
app-rebuild:
	${DC} -f ${APP_FILE} ${ENV} up -d --build

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER}

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} /bin/bash
