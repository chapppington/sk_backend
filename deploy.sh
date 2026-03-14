#!/bin/bash

# Скрипт для деплоя sk_backend на VPS (ветка main)
# Использование: ./deploy.sh

echo "🔎 Checking environment..."
make check-env

echo "🛑 Stopping old containers (prod-down)..."
make prod-down || true

echo "🔨 Building and starting containers (prod-up, without minio and maildev)..."
make prod-up

echo "🧹 Cleaning up old Docker images..."
make clear-old-images

echo "✅ Checking containers status..."
docker ps --filter "name=main-app" --format "table {{.Names}}\t{{.Status}}"
docker ps --filter "name=consumer" --format "table {{.Names}}\t{{.Status}}"

echo "🎉 Deployment completed successfully!"
