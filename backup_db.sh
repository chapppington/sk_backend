#!/usr/bin/env bash
# Бэкап MongoDB из контейнера на локальный сервер

set -e

# Корень проекта: директория со скриптом или выше, где есть .env
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
while [ "$PROJECT_ROOT" != "/" ] && [ ! -f "$PROJECT_ROOT/.env" ]; do
  PROJECT_ROOT="$(dirname "$PROJECT_ROOT")"
done
[ ! -f "$PROJECT_ROOT/.env" ] && PROJECT_ROOT="$SCRIPT_DIR"

BACKUP_DIR="${BACKUP_DIR:-$PROJECT_ROOT/backups}"
CONTAINER_NAME="${MONGO_CONTAINER:-mongodb}"

# Загружаем .env если есть
if [ -f "$PROJECT_ROOT/.env" ]; then
  set -a
  source "$PROJECT_ROOT/.env"
  set +a
fi

MONGO_USER="${MONGO_ROOT_USER:-admin}"
MONGO_PASS="${MONGO_ROOT_PASSWORD:-admin}"
MONGO_DB="${MONGO_DATABASE:-sk}"

mkdir -p "$BACKUP_DIR"
OUTPUT_PATH="$BACKUP_DIR/mongo_${MONGO_DB}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Удаляем старый бэкап, новый перезапишет
rm -rf "$OUTPUT_PATH"

echo "Backup: $CONTAINER_NAME -> $OUTPUT_PATH"

docker exec "$CONTAINER_NAME" mongodump \
  --username="$MONGO_USER" \
  --password="$MONGO_PASS" \
  --authenticationDatabase=admin \
  --db="$MONGO_DB" \
  --out="/tmp/backup_$TIMESTAMP"

docker cp "$CONTAINER_NAME:/tmp/backup_$TIMESTAMP" "$OUTPUT_PATH"
docker exec "$CONTAINER_NAME" rm -rf "/tmp/backup_$TIMESTAMP"

echo "Done: $OUTPUT_PATH"
