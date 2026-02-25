#!/usr/bin/env bash
# Восстановление MongoDB из локального бэкапа (созданного backup_db.sh)

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

RESTORE_PATH="$BACKUP_DIR/mongo_${MONGO_DB}"

if [ ! -d "$RESTORE_PATH" ]; then
  echo "Backup not found: $RESTORE_PATH"
  echo "Run ./backup_db.sh first."
  exit 1
fi

echo "Restore: $RESTORE_PATH -> $CONTAINER_NAME (db: $MONGO_DB)"

docker cp "$RESTORE_PATH" "$CONTAINER_NAME:/tmp/restore"

docker exec "$CONTAINER_NAME" mongorestore \
  --username="$MONGO_USER" \
  --password="$MONGO_PASS" \
  --authenticationDatabase=admin \
  --db="$MONGO_DB" \
  --drop \
  "/tmp/restore/$MONGO_DB"

docker exec "$CONTAINER_NAME" rm -rf "/tmp/restore"

echo "Done."
