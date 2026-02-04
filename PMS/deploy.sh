#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/home/ubuntu/PMS/PMS"
BRANCH="main"

cd "$APP_DIR"

echo ">>> Fetching latest code..."
git fetch origin "$BRANCH"
git reset --hard "origin/$BRANCH"

echo ">>> Building new Docker image..."
docker compose build

echo ">>> Recreating container with new image..."
docker compose up -d --force-recreate

echo ">>> Cleaning up unused images (optional)..."
docker image prune -f

echo ">>> Deployment finished."

